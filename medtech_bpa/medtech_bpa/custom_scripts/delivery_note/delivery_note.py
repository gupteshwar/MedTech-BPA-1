from __future__ import unicode_literals
import frappe
from frappe import _



def validate(doc, method):
	so_name = [row.against_sales_order for row in doc.items if row.against_sales_order]
	if so_name:
		so_doc =frappe.get_doc("Sales Order", so_name[0])
		so_doc.workflow_state = "Pending Dispatch"
		so_doc.db_update()
		frappe.db.commit()


def before_save(doc,method):
	for row in doc.items:
		if row.fully_discount == 1 and row.fully_discount_rate == 0:
			frappe.throw(frappe._("Fully discount rate field is mandatory at row {0}.").format(row.idx))

#!==========================================
#!function for fetching the sales order item wise mrp from sales order


@frappe.whitelist()
def get_mrp_against_sales_order(sales_order,
								item_code):
	mrp_data=frappe.db.get_all("Sales Order Item",filters={"parent":sales_order,"item_code":item_code},
							fields=["custom_mrp"])
	if len(mrp_data)!=0:
		custom_erp = mrp_data[0].get("custom_mrp")
	else:
		custom_erp=None
	return custom_erp

#!============================================
#!==========================================
@frappe.whitelist()
def custom_mrp_against_delivery_note(delivery_note,item_code):
	mrp_data=frappe.db.get_all("Delivery Note Item",
											   filters={"parent":delivery_note,"item_code":item_code},
											   fields=["custom_mrp"])
	if len(mrp_data)!=0:
		custom_erp = mrp_data[0].get("custom_mrp")
	else:
		custom_erp=None
	return custom_erp

