import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
#!Material Transfer for manufacturing Type
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
        order_by='-modified'
        )
    #!Adding Item and Batch Detail
    for stock_entry in stock_entry_list:
        stock_entry_id=stock_entry["name"]
        stock_entry_child_table=frappe.db.get_all("Stock Entry Detail",filters={
            "parent": stock_entry_id},
        fields=["item_code","item_name","description","serial_and_batch_bundle","serial_no","batch_no",
                "uom","qty"]
        )
        stock_entry["item"]=stock_entry_child_table

        
    if len(stock_entry_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=stock_entry_list, message="None", status_code=200)
    if len(stock_entry_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=stock_entry_list, message="None", status_code=200)
    
        
                        
   

