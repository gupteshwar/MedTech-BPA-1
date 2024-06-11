import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllpurchaseReceipt(timestamp="",limit=50,offset=0):

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

    
    purchase_receipt_list = frappe.get_all("Purchase Receipt",
        fields=["name as id",
                "title as title",
                "is_return",
                "supplier",
                "supplier_name",
                "posting_date",
                "supplier_delivery_note",
                "modified as updated_at",
                ],
            
            filters={
                'modified':['>',timestamp],
                 "is_return":0,
            },
            limit=limit,
            order_by='-modified'
        )
    for purchase_receipt in purchase_receipt_list:
        purchase_receipt_id=purchase_receipt["id"]
        purchase_receipt_child_table=frappe.db.get_all("Purchase Receipt Item",filters={
            "parent": purchase_receipt_id},
        fields=["item_code","supplier_part_no","item_name","description",
                "uom","received_qty","qty","rejected_qty","serial_no",
                "serial_and_batch_bundle","rejected_serial_and_batch_bundle",
                "batch_no"
                ]
        )
        purchase_receipt["item"]=purchase_receipt_child_table

        
    if len(purchase_receipt_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=purchase_receipt_list, message="None", status_code=200)
    
        
#!================================================================
#!Purchase Return
import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllpurchaseReturn(timestamp="",limit=50,offset=0):

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

    
    purchase_receipt_list = frappe.get_all("Purchase Receipt",
        fields=["name as id",
                "title as title",
                "is_return",
                "supplier",
                "supplier_name",
                "posting_date",
                "supplier_delivery_note",
                "modified as updated_at",
                ],
            
            filters={
                'modified':['>',timestamp],
                 "is_return":1,
            },
            limit=limit,
            order_by='-modified'
        )
    for purchase_receipt in purchase_receipt_list:
        purchase_receipt_id=purchase_receipt["id"]
        purchase_receipt_child_table=frappe.db.get_all("Purchase Receipt Item",filters={
            "parent": purchase_receipt_id},
        fields=["item_code","supplier_part_no","item_name","description",
                "uom","received_qty","qty","rejected_qty","serial_no",
                "serial_and_batch_bundle","rejected_serial_and_batch_bundle",
                "batch_no"
                ]
        )
        purchase_receipt["item"]=purchase_receipt_child_table

        
    if len(purchase_receipt_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=purchase_receipt_list, message="None", status_code=200)
    
        
                        
   


                        
   

