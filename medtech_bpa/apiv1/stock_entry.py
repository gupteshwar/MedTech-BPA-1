<<<<<<< HEAD
=======
import frappe
from ..api_utils.response import api_response
from datetime import datetime
from frappe import _
from bs4 import BeautifulSoup
from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry
from frappe.desk.form.save import savedocs
#!Paginated Get Customer Details API
#!Material Transfer for manufacturing Type

#!=================================================================================>
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllStockEntryMaterialTransferForManufacturing(timestamp="",limit=50,offset=0):

    #TODO 1: limit offset int format check
    try:
        limit = int(limit)
        offset = int(offset)
    except:
        return api_response(status=False, data=[], message="Please Enter Proper Limit and Offset", status_code=400)
    #!limit and offset upper limit validation
    if limit > 200 or limit < 0 or offset<0:
        return api_response(status=False, data=[], message="Limit exceeded 500", status_code=400)
    #!timestamp non empty validation
    if timestamp is None or timestamp =="":
        return api_response(status=False, data=[], message="Please Enter a timestamp", status_code=400)
    #!timestamp format validation
    try:
        timestamp_datetime=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return api_response(status=False, data=[], message=f"Please Enter a valid timestamp {e}", status_code=400)

    
    stock_entry_list = frappe.get_all("Stock Entry",
        fields=["name","modified as updated_at","posting_date","stock_entry_type","from_warehouse","to_warehouse","docstatus"],
        filters={
                'modified':['>',timestamp],
                'purpose':"Material Transfer for Manufacture"
            },
        limit=limit,
        order_by='-modified',
        start=offset
        )
    #!Adding Item and Batch Detail
    for stock_entry in stock_entry_list:
        stock_entry_id=stock_entry["name"]
        stock_entry_child_table=frappe.db.get_all("Stock Entry Detail",filters={
            "parent": stock_entry_id},
        fields=["item_code","item_name","description","serial_and_batch_bundle","serial_no","batch_no",
                "uom","qty"]
        )
        #!==================================================================================
        for stock_entry_item_data in stock_entry_child_table:
            if stock_entry_item_data.description:
                soup = BeautifulSoup(stock_entry_item_data.description, 'html.parser')
                stock_entry_item_data.description = soup.get_text()
        #!=====================================================================================================
        for stock_entry_items in stock_entry_child_table:
            batch_id=stock_entry_items["batch_no"]
            if batch_id is not None:
                batch_details=frappe.db.get_all("Batch",filters={
                    "name":batch_id
                },fields=["name","qty_to_produce","produced_qty","expiry_date","manufacturing_date"])
                if len(batch_details) > 0:
                    batch_details=batch_details[0]
                    qty_to_produce =batch_details["qty_to_produce"]
                    produced_qty=batch_details["produced_qty"]
                    expiry_date=batch_details["expiry_date"]
                    manufacturing_date=batch_details["manufacturing_date"]

                    stock_entry_items["qty_to_produce"]=qty_to_produce
                    stock_entry_items["produced_qty"]=produced_qty
                    stock_entry_items["expiry_date"]=expiry_date
                    stock_entry_items["manufacturing_date"]=manufacturing_date
                else:
                    stock_entry_items["qty_to_produce"]=0
                    stock_entry_items["produced_qty"]=0
                    stock_entry_items["expiry_date"]=None
                    stock_entry_items["manufacturing_date"]=None
            else:
                stock_entry_items["qty_to_produce"]=0
                stock_entry_items["produced_qty"]=0
                stock_entry_items["expiry_date"]=None
                stock_entry_items["manufacturing_date"]=None
            
        stock_entry["item"]=stock_entry_child_table
    #!==========================================================================================================================
    stock_entry_list_with_timestamp = frappe.get_all("Stock Entry",
        filters={
                'modified':['>',timestamp],
                'purpose':"Material Transfer for Manufacture"
            },
        )   
    data_size=len(stock_entry_list_with_timestamp)
    #!================================================================================================================================ 
    if len(stock_entry_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, 
                            data=stock_entry_list,
                            message="Fetched Stocked Entries Successfully",
                            status_code=200,
                            data_size=data_size)

#!=================================================================================>
@frappe.whitelist(allow_guest=False)
def create_stock_reconciliation(data):
    try:
        data = frappe.parse_json(data)
        
        # Validate company
        company = data.get("company")
        if not company or not frappe.db.exists("Company", company):
            return {"status": "error", "message": _("Invalid company name")}
        
        # Validate items
        items = data.get("items", [])
        if not items:
            return {"status": "error", "message": _("No items provided")}
        
        valid_items = []
        for item in items:
            item_code = item.get("item_code")
            warehouse = item.get("warehouse")
            qty = item.get("qty")
            valuation_rate = item.get("valuation_rate")
            batch_no = item.get("batch_no")  # Optional batch number
            
            if not item_code or not frappe.db.exists("Item", item_code):
                return api_response(status_code=400, message=f"{item_code} is not a valid item", data=[], status=False)
            
            if not warehouse or not frappe.db.exists("Warehouse", warehouse):
                return api_response(status_code=400, message=f"{warehouse} is not a valid warehouse", data=[], status=False)
            
            if qty is None or qty < 0:
                return api_response(status_code=400, message=f"{qty} is not a valid quantity", data=[], status=False)
            
            if valuation_rate is None or valuation_rate < 0:
                return api_response(status_code=400, message=f"{valuation_rate} is not a valid valuation rate", data=[], status=False)
            
            valid_item = {
                "item_code": item_code,
                "warehouse": warehouse,
                "qty": qty,
                "valuation_rate": valuation_rate
            }
            
            if batch_no:
                valid_item["batch_no"] = batch_no
            
            valid_items.append(valid_item)
        
        # Create the Stock Reconciliation document
        doc = frappe.get_doc({
            "doctype": "Stock Reconciliation",
            "company": company,
            "purpose": data.get("purpose", "Stock Reconciliation"),
            "items": valid_items,
        })
        doc.insert()
        doc.submit()
        frappe.db.commit()
        
        return api_response(status_code=200, message="Stock Reconciliation Success", data=doc, status=True)
    except Exception as e:
        return api_response(status_code=400, message=f"Operation error {e}", data=[], status=False)

    
        
                        
   



    
#!=========================================================================================================>
#!Get All Work Orders
#!=================================================================================>
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllWorkOrders(timestamp="",limit=10,offset=0):

    #TODO 1: limit offset int format check
    try:
        limit = int(limit)
        offset = int(offset)
    except:
        return api_response(status=False, data=[], message="Please Enter Proper Limit and Offset", status_code=400)
    #!limit and offset upper limit validation
    if limit > 200 or limit < 0 or offset<0:
        return api_response(status=False, data=[], message="Limit exceeded 500", status_code=400)
    #!timestamp non empty validation
    if timestamp is None or timestamp =="":
        return api_response(status=False, data=[], message="Please Enter a timestamp", status_code=400)
    #!timestamp format validation
    try:
        timestamp_datetime=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return api_response(status=False, data=[], message=f"Please Enter a valid timestamp {e}", status_code=400)

    
    work_order_list = frappe.get_all("Work Order",
        fields=["*"],
        filters={
                'modified':['>',timestamp],
                },
        limit=limit,
        order_by='-modified',
        start=offset
        )
    # #!Adding Item and Batch Detail
    
    for work_order in work_order_list:
        parent_id=work_order.get('name')
        work_order_item=frappe.db.get_all("Work Order Item",filters={'parent':parent_id},fields=["*"])
        for work_order_item_data in work_order_item:
           if work_order_item_data.description:
                soup = BeautifulSoup(work_order_item_data.description, 'html.parser')
                work_order_item_data.description = soup.get_text() 
        work_order["required_items"]=work_order_item     
    #!===================================================================
    work_order_list_with_timestamp = frappe.get_all("Work Order",filters={'modified':['>',timestamp]})
    data_size=len(work_order_list_with_timestamp)
    


    #!===================================================================
    if len(work_order_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, 
                            data=work_order_list, 
                            message="Fetched Work Order List Successfully", 
                            status_code=200,
                            data_size=data_size)
    

# #!========================================================================================================>
@frappe.whitelist(allow_guest=False,methods=["POST"])
def create_stock_entry_manufacturing_against_work_order(work_order_id="",purpose="",qty=""):
    if qty=="":
        return api_response(status_code=400, message=f"Please Enter A Qty", data=[], status=False)
    try:
        qty=int(qty)
    except:
        return api_response(status_code=400, message=f"Please Enter A Valid Qty", data=[], status=False)
    if int(qty)<=0:
        return api_response(status_code=400, message=f"Please Enter A Positive Qty", data=[], status=False)
    if purpose=="":
        return api_response(status_code=400, message=f"Please Enter A Purpose", data=[], status=False)
    if work_order_id=="":
         return api_response(status_code=400, message=f"Please Enter A  Work Order", data=[], status=False)
    if not frappe.db.exists("Work Order",work_order_id):
        return api_response(status_code=400, message=f"Please Enter A Valid Work Order", data=[], status=False)
    work_order=frappe.db.get_all("Work Order",filters={"name":work_order_id},fields=["*"])
    work_order_status=work_order[0].get("status")
    work_order_qty=float(work_order[0].get("qty"))
    produced_qty=float(work_order[0].get("produced_qty"))
    if work_order_status=="Not Started":
        return api_response(status_code=400, message=f"Work Order Must In Process", data=[], status=False)
    
    #!qty validation
    if qty>work_order_qty:
        return api_response(status_code=400, message=f"Work Order Qty Exceeded", data=[], status=False)
    
    #!in work order qty
    #!check quantities left against the work order 
    qty_left =work_order_qty-produced_qty
    if qty>qty_left:
        return api_response(status_code=400, message=f"Qty left to produce exceed", data=[], status=False)

    # stock_entry_list=stock_entry_list_type1+stock_entry_list_type2
    # stock_entry_list=list(set(stock_entry_list))
    #!in stock entry qty
    stock_entry=make_stock_entry(work_order_id=work_order_id,purpose=purpose,qty=qty)
    stock_entry_doc=frappe.get_doc(stock_entry)
    stock_entry_doc.insert()
    stock_entry_doc.submit()
    return api_response(status_code=200, message="Stock Entry Success", data=stock_entry_doc, status=True)
    
>>>>>>> ca0ea29 (api errors fixed and print format with signature and two digit after decimal added)
