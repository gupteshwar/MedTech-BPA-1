import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllDeliveryNote(timestamp="",limit=50,offset=0):

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

    
    delivery_note_list= frappe.get_all("Delivery Note",
        fields=["title as title",
                "is_return",
                "name as id",
                "customer",
                "customer_name",
                "posting_date",
                "address_display as billing_address",
                "shipping_address",
                "pick_list",
                "modified as updated_at",],
            
            filters={
                'modified':['>',timestamp],
                "is_return":0
            },
            limit=limit,
            order_by='-modified'
        )
    #!add customer_details
    for delivery_note in delivery_note_list:

        #!==========================================
        customer=delivery_note["customer"]
        customer_details=frappe.db.get_all("Customer",filters={
            "name":customer},
        fields=["territory"]
        )
        if len(customer_details)!=0:
            customer_location=customer_details[0]["territory"]
        else:
            customer_location=""
        delivery_note["customer_location"]=customer_location
        #!==========================================
        #!add child table items 
        delivery_note_id=delivery_note["id"]
        
        delivery_note_child_table=frappe.db.get_all("Delivery Note Item",filters={
            "parent": delivery_note_id},
        fields=["item_code","item_name","description",
                "uom","qty","serial_no","serial_and_batch_bundle","batch_no","against_sales_invoice"
                ]
        )
        delivery_note["item"]=delivery_note_child_table
        #!adding pick list 
        pick_list_id=delivery_note["pick_list"]
        pick_list_item_details=frappe.db.get_all("Pick List Item",filters={
                    "parent":pick_list_id},
                fields=["item_code","item_name","description","warehouse",
                        "uom","picked_qty","qty","parent"]
                )
        
        delivery_note["pick_list"]=pick_list_item_details
    
      
        
        #!adding sales invoice date and id
        if len(delivery_note_child_table)!=0:
            sales_invoice=delivery_note_child_table[0].get("against_sales_invoice")
            sales_invoice_details=frappe.db.get_all("Sales Invoice",filters={
                "name":sales_invoice},
            fields=["posting_date"]
            )
            if len(sales_invoice_details) > 0:
                delivery_note["sales_invoice"]=sales_invoice[0]
                delivery_note["sales_invoice_date"]=sales_invoice_details[0]["posting_date"]
            else:
                delivery_note["sales_invoice"]=""
                delivery_note["sales_invoice_date"]=""


    if len(delivery_note_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=delivery_note_list, message="None", status_code=200)
    
        
                        
   

#!================================================================

@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllSalesReturn(timestamp="",limit=50,offset=0):

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

    
    delivery_note_list= frappe.get_all("Delivery Note",
        fields=["title as title",
                "is_return",
                "name as id",
                "customer",
                "customer_name",
                "posting_date",
                "address_display as billing_address",
                "shipping_address",
                "pick_list",
                "modified as updated_at",],
            
            filters={
                'modified':['>',timestamp],
                "is_return":1
            },
            limit=limit,
            order_by='-modified'
        )
    #!add customer_details
    for delivery_note in delivery_note_list:

        #!==========================================
        customer=delivery_note["customer"]
        customer_details=frappe.db.get_all("Customer",filters={
            "name":customer},
        fields=["territory"]
        )
        if len(customer_details)!=0:
            customer_location=customer_details[0]["territory"]
        else:
            customer_location=""
        delivery_note["customer_location"]=customer_location
        #!==========================================
        #!add child table items 
        delivery_note_id=delivery_note["id"]
        
        delivery_note_child_table=frappe.db.get_all("Delivery Note Item",filters={
            "parent": delivery_note_id},
        fields=["item_code","item_name","description",
                "uom","qty","serial_no","serial_and_batch_bundle","batch_no","against_sales_invoice"
                ]
        )
        delivery_note["item"]=delivery_note_child_table
        #!adding pick list 
        pick_list_id=delivery_note["pick_list"]
        pick_list_item_details=frappe.db.get_all("Pick List Item",filters={
                    "parent":pick_list_id},
                fields=["item_code","item_name","description","warehouse",
                        "uom","picked_qty","qty","parent"]
                )
        
        delivery_note["pick_list"]=pick_list_item_details
    
      
        
        #!adding sales invoice date and id
        if len(delivery_note_child_table)!=0:
            sales_invoice=delivery_note_child_table[0].get("against_sales_invoice")
            sales_invoice_details=frappe.db.get_all("Sales Invoice",filters={
                "name":sales_invoice},
            fields=["posting_date"]
            )
            if len(sales_invoice_details) > 0:
                delivery_note["sales_invoice"]=sales_invoice[0]
                delivery_note["sales_invoice_date"]=sales_invoice_details[0]["posting_date"]
            else:
                delivery_note["sales_invoice"]=""
                delivery_note["sales_invoice_date"]=""


    if len(delivery_note_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=delivery_note_list, message="None", status_code=200)
    
        
                        
   

