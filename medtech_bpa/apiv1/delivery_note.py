import frappe
from ..api_utils.response import api_response
from datetime import datetime
from bs4 import BeautifulSoup
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllDeliveryNote(timestamp="",limit=50,offset=0):
    #!STANDARD VALIDATION================================================================>
    #TODO 1: limit offset int format check
    try:
        limit = int(limit)
        offset = int(offset)
    except:
        return api_response(status=False, data=[], message="Please Enter Proper Limit and Offset", status_code=400)
    #!limit and offset upper limit validation
    if limit > 200 or limit < 0 or offset<0:
        return api_response(status=False, data=[], message="Limit exceeded 200", status_code=400)
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
                "transporter",
                "vehicle_no",
                "driver",
                "mode_of_transport",
                "gst_vehicle_type",
                "lr_no",
                "gst_transporter_id",
                "custom_consignee_name as consignee_name",
                "custom_consignee_city as consignee_city",
                "custom_consignee_state as consignee_state",
                "custom_consignee_country as consignee_country",
                "custom_consignee_postal_code as consignee_postal_code",
                "custom_consignee_contact as consignee_contact",
                "custom_consignee_address_ as consignee_address",
                "modified as updated_at"],
            
            filters={
                'modified':['>',timestamp],
                "is_return":0
            },
            limit=limit,
            start=offset,
            order_by='-modified'
        )
   
    for delivery_note in delivery_note_list:
        delivery_note_id=delivery_note.get("id")
        linked_sales_invoice=frappe.db.get_all("Sales Invoice",filters={"delivery_note":delivery_note_id},fields=["name","posting_date"])
        delivery_note["sales_invoice_data"]=linked_sales_invoice

    for delivery_note in delivery_note_list:
        #!=============================================
        #!parsing addresses
        if delivery_note.billing_address is not None and len(delivery_note.billing_address)>0:
            soup1 = BeautifulSoup(delivery_note.billing_address, 'html.parser')
            delivery_note.billing_address = soup1.get_text()
        if delivery_note.shipping_address is not None and len(delivery_note.shipping_address)>0:
            soup2= BeautifulSoup(delivery_note.shipping_address, 'html.parser')
            delivery_note.shipping_address=soup2.get_text()
        #!================================================
        #!2 add customer_details    
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
        #!=============================================================================
        #!Parsing Description
        for delivery_note_items in delivery_note_child_table:
           if delivery_note_items.description and len(delivery_note_items.description) > 0:
                soup = BeautifulSoup(delivery_note_items.description, 'html.parser')
                delivery_note_items.description = soup.get_text() 
        #!==============================================================================
        #! Adding Item Child Table  and batch details
    
        for delivery_note_items in delivery_note_child_table:
            batch_id=delivery_note_items["batch_no"]
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

                    delivery_note_items["qty_to_produce"]=qty_to_produce
                    delivery_note_items["produced_qty"]=produced_qty
                    delivery_note_items["expiry_date"]=expiry_date
                    delivery_note_items["manufacturing_date"]=manufacturing_date
                else:
                    delivery_note_items["qty_to_produce"]=0
                    delivery_note_items["produced_qty"]=0
                    delivery_note_items["expiry_date"]=None
                    delivery_note_items["manufacturing_date"]=None

            else:
                delivery_note_items["qty_to_produce"]=0
                delivery_note_items["produced_qty"]=0
                delivery_note_items["expiry_date"]=None
                delivery_note_items["manufacturing_date"]=None
        delivery_note["item"]=delivery_note_child_table

        #!Adding item stock

    #!====================================================================
    delivery_note_list_with_timestamp= frappe.get_all("Delivery Note",
            filters={'modified':['>',timestamp],"is_return":0
            },
         
        )
    data_size=len(delivery_note_list_with_timestamp)
    #!=====================================================================
    if len(delivery_note_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, 
                            data=delivery_note_list, 
                            message="Successfully Fetched Delivery Note",
                            status_code=200,
                            data_size=data_size
                            )
    
        
                        
   

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
        return api_response(status=False, data=[], message="Limit exceeded 200", status_code=400)
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
            start=offset,
            order_by='-modified'
        )
    #!add customer_details
    for delivery_note in delivery_note_list:
        #!=============================================
        #!parsing addresses
        if delivery_note.billing_address:
            soup = BeautifulSoup(delivery_note.billing_address, 'html.parser')
            delivery_note.billing_address = soup.get_text()
        if delivery_note.shipping_address:
            soup= BeautifulSoup(delivery_note.shipping_address, 'html.parser')
            delivery_note.shipping_address=soup.get_text()
        #!================================================
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
        #!=============================================================================
        #!Parsing Description
        for delivery_note_items in delivery_note_child_table:
           if delivery_note_items.description:
                soup = BeautifulSoup(delivery_note_items.description, 'html.parser')
                delivery_note_items.description = soup.get_text() 
        #!==============================================================================
        for delivery_note_items in delivery_note_child_table:
            batch_id=delivery_note_items["batch_no"]
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

                    delivery_note_items["qty_to_produce"]=qty_to_produce
                    delivery_note_items["produced_qty"]=produced_qty
                    delivery_note_items["expiry_date"]=expiry_date
                    delivery_note_items["manufacturing_date"]=manufacturing_date
                else:
                    delivery_note_items["qty_to_produce"]=0
                    delivery_note_items["produced_qty"]=0
                    delivery_note_items["expiry_date"]=None
                    delivery_note_items["manufacturing_date"]=None
            else:
                delivery_note_items["qty_to_produce"]=0
                delivery_note_items["produced_qty"]=0
                delivery_note_items["expiry_date"]=None
                delivery_note_items["manufacturing_date"]=None
        delivery_note["item"]=delivery_note_child_table
        #!adding pick list 

        
    
      
        
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
    #!====================================================================
    sales_return_list_with_timestamp= frappe.get_all("Delivery Note",
            filters={'modified':['>',timestamp],"is_return":1
            },
         
        )
    data_size=len(sales_return_list_with_timestamp)
    #!=====================================================================

    if len(delivery_note_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, 
                            data=delivery_note_list, message="Fetched All Sales Return ", status_code=200,data_size=data_size)
    
        
                        
   

#!==============================================================>

@frappe.whitelist(allow_guest=False,methods=["POST"])
def create_delivery_note_confirmation(
                        delivery_note="",
                        dispatch_order_date="",
                        dispatch_order_number="",
                        customer_code="",
                        item_code="",
                        batch_no="",
                        org_code="",
                        bin_code="",
                        dispatch_qty="",
                        process_flag="",
                        error_desc="",
                        sub_inventory="",
                        pick_list=""
                      ):
            
            
            if delivery_note=="":
                return api_response(status=True, data=[], message="Enter Delivery Note", status_code=400)
            if dispatch_order_number=="":
                return api_response(status=True, data=[], message="Enter Dispatch Order Number", status_code=400)
            
            confirmation_list=frappe.db.get_all("confirm Delivery Note Item Wise Batch Wise",
                                                filters={"delivery_note": delivery_note,
                                                         "item_code": item_code,})
            if len(confirmation_list)>0:
                return api_response(status=True, data=[], message="Delivery Note Item Wise Batch Wise Already Exists", status_code=400)
            # if customer_code=="":
            #     return api_response(status=True, data=[], message="Enter Item Code", status_code=400)
            # if sub_inventory=="":
            #     return api_response(status=True, data=[], message="Enter Sub Inventory", status_code=400)
            # if org_code=="":
            #     return api_response(status=True, data=[], message="Enter Organization Code", status_code=400)
            # if bin_code=="":
            #     return api_response(status=True, data=[], message="Enter Bin No", status_code=400)
            # if batch_no=="":
            #     return api_response(status=True, data=[], message="Enter Batch No", status_code=400)
            if dispatch_qty=="":
                return api_response(status=True, data=[], message="Enter Qty", status_code=400)
            if process_flag=="":
                return api_response(status=True, data=[], message="Enter Process Flag", status_code=400)
            if dispatch_order_date=="":
                return api_response(status=True, data=[], message="Enter Rec Entry Date", status_code=400)
            try:
                dispatch_qty = int(dispatch_qty)
            except:
                return api_response(status=False, data=[], message="Please Enter Proper DispatchQty", status_code=400)
            try:
                dispatch_order_date = datetime.strptime(dispatch_order_date, '%Y-%m-%d')
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Dispatch Order Date", status_code=400)
            #!================================================================================================================>
            if pick_list !="" and not frappe.db.exists("Pick List",pick_list):
                return api_response(status=False, data=[], message="Pick List Does Not Exist", status_code=400)
            if not frappe.db.exists("Delivery Note",delivery_note):
                return api_response(status=False, data=[], message="Delivery Note Does Not Exist", status_code=400)
            if customer_code!="":
                if not frappe.db.exists("Customer",customer_code):
                    return api_response(status=False, data=[], message="Customer Does Not Exist", status_code=400)
            if not frappe.db.exists("Item",item_code):
                return api_response(status=False, data=[], message="Item Does Not Exist", status_code=400)
            #!================================================================================================================>
            try:
       
                doc = frappe.get_doc({
                            "doctype": "confirm Delivery Note Item Wise Batch Wise",
                            "delivery_note": delivery_note,
                            "dispatch_order_date": dispatch_order_date,
                            "dispatch_order_number": dispatch_order_number,
                            "customer_code": customer_code,
                            "item_code": item_code,
                            "batch_no": batch_no,
                            "org_code": org_code,
                            "bin_code": bin_code,
                            "subinventory": sub_inventory,
                            "dispatch_qty": dispatch_qty,
                            "process_flag": process_flag,
                            "error_desc": error_desc,
                            "pick_list": pick_list
                        })
                doc.insert()
                frappe.db.commit()
                return api_response(status=True,data=doc,message="Successfully Created Document",status_code=200)
            except Exception as e:
                    frappe.db.rollback()
                    return api_response(status=False,data='',message="Operation Failed",status_code=500)

            
            
            
            

# #!Paginated Get Customer Details API
# @frappe.whitelist(allow_guest=False,methods=["GET"])
# def getSalesInvoice(timestamp="",limit=100,offset=0):

#     #TODO 1: limit offset int format check
#     try:
#         limit = int(limit)
#         offset = int(offset)
#     except:
#         return api_response(status=False, data=[], message="Please Enter Proper Limit and Offset", status_code=400)
#     #!limit and offset upper limit validation
#     if limit > 200 or limit < 0 or offset<0:
#         return api_response(status=False, data=[], message="Limit exceeded 500", status_code=400)
#     #!timestamp non empty validation
#     if timestamp is None or timestamp =="":
#         return api_response(status=False, data=[], message="Please Enter a timestamp", status_code=400)
#     #!timestamp format validation
#     try:
#         timestamp_datetime=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
#     except Exception as e:
#         return api_response(status=False, data=[], message=f"Please Enter a valid timestamp {e}", status_code=400)

#     item_group_list = frappe.get_all("Sales Invoice",
#         fields=["name","delivery_note"
#                 ],
            
#             filters={
#                 'modified':['>',timestamp]
#             },
#             limit=limit,
#             start=offset,
#             order_by='-modified'
#         )
#     #!==========================================================================================
#     #!==========================================================================================
#     item_group_list_time_stamp = frappe.get_all("Item Group",filters={'modified':['>',timestamp]} )
#     data_size=len(item_group_list_time_stamp)

#     #!=========================================================================================
#     if len(item_group_list)==0:
#         return api_response(status=True, data=[], message="Empty Content", status_code=204)
#     else:
#         return api_response(status=True, 
#                             data=item_group_list, 
#                             message="Successfully Fetched Item Groups", 
#                             status_code=200,
#                             data_size=data_size)
       
            

    
