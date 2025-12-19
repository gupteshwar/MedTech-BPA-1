import json
import frappe
from frappe import _
from frappe.utils import getdate, flt
from frappe.utils.background_jobs import enqueue
from frappe.utils import nowdate, add_days



@frappe.whitelist()
def send_so_notification(sales_order):
    try:
        so = frappe.get_doc("Sales Order", sales_order)
        #get email ids
        recipients = [frappe.db.get_value("Customer", so.customer, "email_id")]
        cc = []
        for row in so.sales_team:
            if row.sales_person:
                sp_email = frappe.db.get_value("Sales Person", row.sales_person,\
                    "contact_company_email")
                if sp_email:
                    cc.append(sp_email)

        if not recipients and not cc:
            frappe.msgprint("Please add email Ids for Customer and Sales Persons")
        else:
            subject = "Sales Order {} Notification".format(so.name)
            message = "Hi,\t This is system generated message. Do not reply.\n\
            In case of query, check with your System Administrative"

            email_args = {
                "recipients": ['sangram.p@indictranstech.com'], #recipients,
                "sender": None,
                "subject": subject,
                "message": message,
                "now": True,
                "attachments": [frappe.attach_print("Sales Order", so.name)]
            }
            enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
        return so.name
    except Exception as e:
        print("#####################\n {}".format(str(e)))
        #frappe.msgprint("Error: {}".format(str(e)))

def on_update_after_submit(doc,method):
    try:
        if doc.workflow_state == 'Payment Pending':
            #get email ids
            recipients = [frappe.db.get_value("Customer", doc.customer, "email_id")]
            cc = []
            for row in doc.sales_team:
                if row.sales_person:
                    sp_email = frappe.db.get_value("Sales Person", row.sales_person,
                        "contact_company_email")
                    if sp_email:
                        cc.append(sp_email)

            if not recipients and not cc:
                frappe.msgprint("Please add email Ids for Customer and Sales Persons")
            else:
                subject = "Sales Order {} Notification".format(doc.name)
                message = "Hi,\t This is system generated message. Do not reply.\n\
                In case of query, check with your System Administrative"

                email_args = {
                    "recipients": recipients, 
                    "cc" : cc,
                    "sender": None,
                    "subject": subject,
                    "message": message,
                    "now": True,
                    "attachments": [frappe.attach_print("Sales Order", doc.name)]
                }
                enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
            return doc.name
    except Exception as e:
        print("#####################\n {}".format(str(e)))
        #frappe.msgprint("Error: {}".format(str(e)))


def validate(doc, method):
    pricing_rule = frappe.db.get_values("Pricing Rule", {"customer":doc.customer, "is_cummulative_customer":1}, ["max_amt", "valid_from", "valid_upto", "discount_percentage"],as_dict=1)

    if pricing_rule:
        so_details = frappe.db.sql("""SELECT name, grand_total, discount_amount from `tabSales Order` where transaction_date>='{0}' and transaction_date<='{1}' and customer='{2}'""".format(pricing_rule[0].get('valid_from'), pricing_rule[0].get('valid_upto'), doc.customer), as_dict=1)
        discount_calculation(doc, so_details, pricing_rule)


def discount_calculation(doc, so_details, pricing_rule):
    total_amt=0.0
    total_amt+=doc.grand_total
    disc_amt = 0.0
    so_name = []
    for row in so_details:
        if row.get("discount_amount")>0:
            so_name.append(row.name)

    if getdate(doc.transaction_date) >= getdate(pricing_rule[0].get('valid_from')) and getdate(doc.transaction_date) <= getdate(pricing_rule[0].get('valid_upto')):
        if so_name:
            disc_amt = doc.grand_total*pricing_rule[0].get("discount_percentage")/100 
            doc.discount_amount = disc_amt
            doc.grand_total = doc.grand_total-disc_amt
            doc.rounded_total = round(doc.grand_total)
            in_words = frappe.utils.money_in_words(round(doc.grand_total))
            doc.in_words = in_words
        else:
            for row in so_details:
                total_amt+=row.grand_total
                if total_amt >= pricing_rule[0].get("max_amt") and not doc.discount_amount:
                    disc_amt = total_amt*pricing_rule[0].get("discount_percentage")/100 
                    doc.discount_amount = disc_amt
                    doc.grand_total = doc.grand_total-disc_amt
                    doc.rounded_total = round(doc.grand_total)
                    in_words = frappe.utils.money_in_words(round(doc.grand_total))
                    doc.in_words = in_words

def update_rate_with_taxes(doc, method):
    item_taxes = frappe._dict()
    # get item_wise_taxes
    if doc.taxes_and_charges or len(doc.get("taxes")):
        for tax in doc.get("taxes"):
            if tax.item_wise_tax_detail:
                tax_detail = json.loads(tax.item_wise_tax_detail)
                for k, v in tax_detail.items():
                    if not k in item_taxes:
                        item_taxes[k] = flt(v[1])
                    else:
                        item_taxes[k] = item_taxes.get(k, 0) + flt(v[1])

    #update item table with tax rate
    for item in doc.get("items"):
        if item.rate:
            tax_amt = item_taxes.get(item.item_code) or item_taxes.get(item.item_name)
            if tax_amt and tax_amt > 0:
                item.rate_with_tax = item.rate + flt(tax_amt/item.qty)
            else:
                item.rate_with_tax = item.rate
    doc.flags.ignore_permissions = True
    #doc.save()


@frappe.whitelist()
def reason_of_rejection(reason, name):
    doc = frappe.new_doc("Comment")
    doc.comment_type = "Comment"
    doc.reference_doctype = "Sales Order"
    doc.reference_name = name
    doc.comment_email = frappe.session.user
    doc.comment_by = frappe.db.get_value("User", {'name':frappe.session.user}, 'full_name')
    doc.content = reason
    doc.save()

    return True

def before_save(doc,method):
    for row in doc.items:
        if row.fully_discount == 1 and row.fully_discount_rate == 0:
            frappe.throw(frappe._("Fully discount rate field is mandatory at row {0}.").format(row.idx))

# @frappe.whitelist()
# def get_bom_materials_for_sales_order_item(sales_order):
#     so = frappe.get_doc("Sales Order", sales_order)
#     result = []

#     for item in so.items:
#         sales_order_item = item.name
        
#         bom = frappe.get_doc("BOM", item.bom_no)
#         for bom_item in bom.items:
#             result.append({
              
#                 "item_code": bom_item.item_code,
#                 "qty": bom_item.qty * item.qty,
#                 "uom": bom_item.uom,
#                 "rate":bom_item.rate,
#                 "amount":bom_item.amount,
#                 "sales_order_item":sales_order_item
#             })
   
#     return result

# API to create MR for RM 
@frappe.whitelist()
def create_material_request_from_bom(sales_order):
    sales_order_doc = frappe.get_doc("Sales Order", sales_order)
    source_warehouses = [
        "Vapi GST - RAW MATERIAL - MLPL",
        "Vapi-Concessional Godown - MLPL",
    ]
    target_warehouse = "Vapi Reserved stock Godown - MLPL"
    mr_rows = []

    # Create pending records if not exist
    for so_item in sales_order_doc.items:
        bom_name = frappe.db.get_value("BOM", {"item": so_item.item_code, "is_default": 1, "is_active": 1}, "name")
        if not bom_name: continue
        bom_doc = frappe.get_doc("BOM", bom_name)
        
        for rm in bom_doc.items:
            required_qty = rm.qty * so_item.qty
            rm_item_name = frappe.db.get_value("Item", rm.item_code, "item_name")

            pending_doc = frappe.db.get_value(
                "Sales Order RM Pending",
                {"sales_order": sales_order, "item_code": rm.item_code, "company": sales_order_doc.company},
                ["pending_qty"], as_dict=True
            )
            if not pending_doc:
                frappe.get_doc({
                    "doctype": "Sales Order RM Pending",
                    "company": sales_order_doc.company,
                    "sales_order": sales_order,
                    "item_code": rm.item_code,
                    "raw_material_name": rm_item_name,
                    "fg_item_code": so_item.item_code,
                    "required_qty": required_qty,
                    "pending_qty": required_qty,
                    "issued_qty": 0,
                    "uom": rm.uom
                }).insert(ignore_permissions=True)

    #Fetch pending items
    pending_items = frappe.get_all(
        "Sales Order RM Pending",
        filters={"sales_order": sales_order, "company": sales_order_doc.company, "pending_qty": (">", 0)},
        fields=["item_code", "pending_qty", "uom"]
    )
    if not pending_items:
        frappe.throw("No pending RM for this Sales Order.")

    #Allocate stock from WH1, WH2
    for row in pending_items:
        remaining = row.pending_qty
        item_name = frappe.db.get_value("Item", row.item_code, "item_name") or row.item_code

        for wh in source_warehouses:
            if remaining <= 0: break
            stock = frappe.db.get_value("Bin", {"item_code": row.item_code, "warehouse": wh}, "actual_qty") or 0
            if stock <= 0: continue
            take = min(stock, remaining)
            frappe.log_error(f"[DEBUG] Allocating {take} of {row.item_code} from {wh}, Pending: {remaining}", "MR Allocation")
            mr_rows.append({
                "item_code": row.item_code,
                "item_name": item_name,
                "qty": take,
                "uom": row.uom,
                "from_warehouse": wh,
            })
            remaining -= take

    #Create MR
    if not mr_rows:
        frappe.throw("No stock available to create Material Request.")

    mr = frappe.new_doc("Material Request")
    mr.material_request_type = "Material Transfer"
    mr.company = sales_order_doc.company
    mr.sales_order = sales_order
    mr.required_by = frappe.utils.today()
    mr.custom_created_from_material_request_for_rm_button = 1

    for row in mr_rows:
        mr.append("items", {
            "item_code": row["item_code"],
            "item_name": row["item_name"],
            "qty": row["qty"],
            "uom": row["uom"],
            "from_warehouse": row["from_warehouse"],
            "warehouse": target_warehouse,
            "schedule_date": frappe.utils.today(),
            "sales_order": sales_order,
        })

    mr.insert(ignore_permissions=True)
    frappe.db.commit()
    return mr.name
