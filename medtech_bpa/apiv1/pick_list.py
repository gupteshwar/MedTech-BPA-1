import frappe
from ..api_utils.response import api_response
from datetime import datetime
from bs4 import BeautifulSoup
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllPickList(timestamp="",limit=50,offset=0):
    #!STANDARD VALIDATION================================================================>
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

    
    pick_list_list= frappe.get_all("Pick List",
        fields=["name as name",
                "company",
                "purpose",
                "customer",
                "customer_name",
                "work_order",
                "material_request",
                "for_qty",
                "parent_warehouse",
                "modified as updated_at",
                "docstatus",],
            
            filters={
                'modified':['>',timestamp],
            },
            limit=limit,
            start=offset,
            order_by='-modified'
        )
   
        
    #!attach picklist item
    for pick_list in pick_list_list:
        parent_id=pick_list.get("name")
        pick_list_item=frappe.db.get_all("Pick List Item",filters={"parent":parent_id},fields=["*"])
        for pick_list_item_data in pick_list_item:
           if pick_list_item_data.description:
                soup = BeautifulSoup(pick_list_item_data.description, 'html.parser')
                pick_list_item_data.description = soup.get_text() 
                qty=pick_list_item_data.qty
                stock_qty=pick_list_item_data.stock_qty
                picked_qty=pick_list_item_data.picked_qty
                if qty is not None:
                     qty=format(float(qty), 'f')
                     pick_list_item_data.qty=qty
                if stock_qty is not None:
                     stock_qty=format(float(stock_qty), 'f')
                     pick_list_item_data.stock_qty=stock_qty
                    
                if picked_qty is not None:
                     picked_qty=format(float(picked_qty), 'f')
                     pick_list_item_data.picked_qty=picked_qty  # converting to float to avoid scientific notation
                
                # #!to float
                # "qty": 5e-05,
                # "stock_qty": 5e-05,
                # "picked_qty": 5e-05,

        pick_list["items"]=pick_list_item

        #!Adding item stock
    #!attaching delivery note id 
    for pick_list in pick_list_list:
        delivery_note=frappe.db.get_all("Delivery Note", filters={"pick_list":pick_list.get("name")}, fields=["name"])
        if len(delivery_note) > 0:
             delivery_note=delivery_note[0].get("name")
        else:
             delivery_note=None  # if no delivery note found set it to None
        pick_list["delivery_note"]=delivery_note
        
    #!attach
    #!==================================================
    pick_list_list_with_timestamp= frappe.get_all("Pick List",
            filters={
                'modified':['>',timestamp],
            },
        )
    data_size=len(pick_list_list_with_timestamp)
    if len(pick_list_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, 
                            data=pick_list_list, 
                            message="Successfully fetched Picklist List", 
                            status_code=200,
                            data_size=data_size)
    
        
                        
   

            
            
#!Item  Wise Batch wise Pick List Confirmation

@frappe.whitelist(allow_guest=False,methods=["POST"])
def create_pick_list_confirmation(
                        pick_list="",
                        pick_list_date="",
                        customer_code="",
                        item="",
                        qty="",
                        batch_no="",
                        org_code="",
                        bin_code="",
                        process_flag=0,
                        error_desc="",
                        sub_inventory="",
                        pick_list_purpose="",
                        delivery_note="",
                      ):
            

            #!=======================================================================================
            if item=="":
                return api_response(status=True, data=[], message="Enter Item Code", status_code=400)
            if qty=="":
                 return api_response(status=True, data=[], message="Enter Qty", status_code=400)
            if pick_list=="":
                return api_response(status=True, data=[], message="Enter Delivery Note", status_code=400)
            if pick_list_date=="":
                return api_response(status=True, data=[], message="Enter Dispatch Order Number", status_code=400)
            if process_flag=="":
                return api_response(status=True, data=[], message="Enter Process Flag", status_code=400)
            try:
                qty=int(qty)
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Qty", status_code=400)
            if  qty<=0:
                 return api_response(status=False, data=[], message="Please Enter Positive Qty", status_code=400)
            try:
                pick_list_date = datetime.strptime(pick_list_date, '%Y-%m-%d')
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Dispatch Order Date", status_code=400)
            #!================================================================================================================>
            if not frappe.db.exists("Pick List",pick_list):
                return api_response(status=False, data=[], message="Pick List Does Not Exist", status_code=400)
            if not frappe.db.exists("Item",item):
                return api_response(status=False, data=[], message="Item Does Not Exist", status_code=400)
            if customer_code!="" and not frappe.db.exists("Customer",customer_code):
                    return api_response(status=False, data=[], message="Customer Does Not Exist", status_code=400)
            if delivery_note!="" and not frappe.db.exists("Delivery Note",delivery_note):
                 return api_response(status=False, data=[], message="Delivery Note Does Not Exist", status_code=400)
            

            #!if item exist in pick list
            item_in_pick_list=frappe.db.get_all("Pick List Item",filters={
                 "parent": pick_list,
                 "item_code": item
                 }
             )
            if len(item_in_pick_list)==0:
                 return api_response(status=False, data=[], message="Item Doesn't Exist in Pick List", status_code=400)
            
            #!filter of purchase receipt qty per item and validating against confirmation qty
            #!===============================================================================
            #!===============================================================================
            #!===============================================================================
            pick_list_item_data=frappe.db.get_all("Pick List Item",filters={"parent":pick_list,"item_code":item},fields=["qty"])
            if len(pick_list_item_data)!=0:
                picked_list_item_qty=pick_list_item_data[0].qty
            else:
                picked_list_item_qty=None

            confirmation_list=frappe.db.get_all("Pick List Item Wise Batch Wise Confirmation",
                                                filters={"pick_list": pick_list,
                                                           "item": item},
                                                fields=["qty"])

            #!====================================================
            #!if no confirmation quantity and purchase quantity then no validation required
            if len(confirmation_list)>0:
                confirmed_qty=0
                for confirmation in confirmation_list:
                    confirmed_qty+=float(confirmation.qty)
            else:
                confirmed_qty=None
            #!====================================================
            if picked_list_item_qty is not None:
                if confirmed_qty is not None:
                    quantity_left_to_confirm=float(picked_list_item_qty)-float(confirmed_qty)
                    if float(qty)>float(quantity_left_to_confirm):
                        return api_response(status=False, data=[], message="Remaining Confirmation Quantity Exceeds Qty  Pick List Qty", status_code=400)
                else:
                    if float(qty)>float(picked_list_item_qty):
                        return api_response(status=False, data=[], message="Confirmation Quantity Exceeds Qty Pick List Qty",status_code=400)
           
            
            #!====================================================
            #!====================================================
            #!====================================================
            
            #!====================================================
            #!====================================================
            #!====================================================
            
            try:
       
                doc = frappe.get_doc({
                            "doctype": "Pick List Item Wise Batch Wise Confirmation",
                            "pick_list": pick_list,
                            "pick_list_date": pick_list_date,
                            "customer_code": customer_code,
                            "item": item,
                            "batch_no": batch_no,
                            "org_code": org_code,
                            "bin_code": bin_code,
                            "sub_inventory": sub_inventory,
                            "qty":qty,
                            "process_flag": process_flag,
                            "error_desc": error_desc,
                            "picked_list_purpose":pick_list_purpose,
                            "delivery_note":delivery_note
                        })
                doc.insert()
                frappe.db.commit()
                return api_response(status=True,data=doc,message="Successfully Created Document",status_code=200)
            except Exception as e:
                    frappe.db.rollback()
                    return api_response(status=False,data='',message="Operation Failed",status_code=500)

            
            
#!----------------------------------------------------------------------------------------
#!COMMIT
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllProductionPickList(timestamp="",limit=50,offset=0):
    #!STANDARD VALIDATION================================================================>
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

    
    pick_list_list= frappe.get_all("Production Pick List",
        fields=["name as name",
                "company",
                "purpose",
                "branch",
                "customer",
                "work_order",
                "production_plan",
                "material_request",
                "for_qty",
                "material_request",
                "parent_warehouse",
                "modified as updated_at",
                "docstatus",],
            
            filters={
                'modified':['>',timestamp],
            },
            limit=limit,
            start=offset,
            order_by='-modified'
        )
   
        
    #!attach picklist item
    for pick_list in pick_list_list:
        parent_id=pick_list.get("name")
        pick_list_item=frappe.db.get_all("Production Pick List Item",filters={"parent":parent_id},fields=["*"])
        for pick_list_item_data in pick_list_item:
           if pick_list_item_data.description:
                soup = BeautifulSoup(pick_list_item_data.description, 'html.parser')
                pick_list_item_data.description = soup.get_text() 
                qty=pick_list_item_data.qty
                stock_qty=pick_list_item_data.stock_qty
                picked_qty=pick_list_item_data.picked_qty
                if qty is not None:
                     qty=format(float(qty), 'f')
                     pick_list_item_data.qty=qty
                if stock_qty is not None:
                     stock_qty=format(float(stock_qty), 'f')
                     pick_list_item_data.stock_qty=stock_qty
                    
                if picked_qty is not None:
                     picked_qty=format(float(picked_qty), 'f')
                     pick_list_item_data.picked_qty=picked_qty  # converting to float to avoid scientific notation
                
                # #!to float
                # "qty": 5e-05,
                # "stock_qty": 5e-05,
                # "picked_qty": 5e-05,

        pick_list["items"]=pick_list_item

        #!Adding item stock
    #!attaching delivery note id 
    for pick_list in pick_list_list:
        delivery_note=frappe.db.get_all("Delivery Note", filters={"pick_list":pick_list.get("name")}, fields=["name"])
        if len(delivery_note) > 0:
             delivery_note=delivery_note[0].get("name")
        else:
             delivery_note=None  # if no delivery note found set it to None
        pick_list["delivery_note"]=delivery_note
        
    #!attach
    #!==================================================
    pick_list_list_with_timestamp= frappe.get_all("Production Pick List Item",
            filters={
                'modified':['>',timestamp],
            },
        )
    data_size=len(pick_list_list_with_timestamp)
    if len(pick_list_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, 
                            data=pick_list_list, 
                            message="Successfully fetched Picklist List", 
                            status_code=200,
                            data_size=data_size)                        
   



#!==================================================================================
@frappe.whitelist(allow_guest=False,methods=["POST"])
def create_production_pick_list_confirmation(
                        pick_list="",
                        pick_list_date="",
                        customer_code="",
                        item="",
                        qty="",
                        batch_no="",
                        org_code="",
                        bin_code="",
                        process_flag=0,
                        error_desc="",
                        sub_inventory="",
                        pick_list_purpose="",
                        delivery_note="",
                      ):
            

            #!=======================================================================================
            if item=="":
                return api_response(status=False, data=[], message="Enter Item Code", status_code=400)
            if qty=="":
                 return api_response(status=False, data=[], message="Enter Qty", status_code=400)
            if pick_list=="":
                return api_response(status=False, data=[], message="Enter Delivery Note", status_code=400)
            if pick_list_date=="":
                return api_response(status=False, data=[], message="Enter Dispatch Order Number", status_code=400)
            if process_flag=="":
                return api_response(status=False, data=[], message="Enter Process Flag", status_code=400)
            try:
                qty=int(qty)
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Qty", status_code=400)
            if  qty<0:
                 return api_response(status=False, data=[], message="Please Enter Positive Qty", status_code=400)
            try:
                pick_list_date = datetime.strptime(pick_list_date, '%Y-%m-%d')
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Dispatch Order Date", status_code=400)
            #!================================================================================================================>
            if not frappe.db.exists("Production Pick List",pick_list):
                return api_response(status=False, data=[], message="Production Pick List Does Not Exist", status_code=400)
            if not frappe.db.exists("Item",item):
                return api_response(status=False, data=[], message="Item Does Not Exist", status_code=400)
            if customer_code!="" and not frappe.db.exists("Customer",customer_code):
                    return api_response(status=False, data=[], message="Customer Does Not Exist", status_code=400)
            if delivery_note!="" and not frappe.db.exists("Delivery Note",delivery_note):
                 return api_response(status=False, data=[], message="Delivery Note Does Not Exist", status_code=400)
            

            #!if item exist in pick list
            item_in_pick_list=frappe.db.get_all("Production Pick List Item",filters={
                 "parent": pick_list,
                 "item_code": item
                 }
             )
            if len(item_in_pick_list)==0:
                 return api_response(status=False, data=[], message="Item Doesn't Exist in Production Pick List", status_code=400)
            
            #!filter of purchase receipt qty per item and validating against confirmation qty
            #!===============================================================================
            #!===============================================================================
            #!===============================================================================
            pick_list_item_data=frappe.db.get_all("Production Pick List Item",filters={"parent":pick_list,"item_code":item},fields=["qty"])
            if len(pick_list_item_data)!=0:
                picked_list_item_qty=pick_list_item_data[0].qty
            else:
                picked_list_item_qty=None

            confirmation_list=frappe.db.get_all("Pick List Item Wise Batch Wise Confirmation",
                                                filters={"production_pick_list": pick_list,
                                                           "item": item},
                                                fields=["qty"])

            #!====================================================
            #!if no confirmation quantity and purchase quantity then no validation required
            if len(confirmation_list)>0:
                confirmed_qty=0
                for confirmation in confirmation_list:
                    confirmed_qty+=float(confirmation.qty)
            else:
                confirmed_qty=None
            #!====================================================
            if picked_list_item_qty is not None:
                if confirmed_qty is not None:
                    quantity_left_to_confirm=float(picked_list_item_qty)-float(confirmed_qty)
                    if float(qty)>float(quantity_left_to_confirm):
                        return api_response(status=False, data=[], 
                                            message="Remaining Confirmation Quantity Exceeds Qty  Pick List Qty",
                                            status_code=400)
                else:
                    if float(qty)>float(picked_list_item_qty):
                        return api_response(status=False, data=[], 
                                            message="Confirmation Quantity Exceeds Qty Pick List Qty",
                                            status_code=400)
           
            
            #!====================================================
            #!====================================================
            #!====================================================
            
            #!====================================================
            #!====================================================
            #!====================================================
            
            try:
       
                doc = frappe.get_doc({
                            "doctype": "Pick List Item Wise Batch Wise Confirmation",
                            "production_pick_list": pick_list,
                            "pick_list_date": pick_list_date,
                            "customer_code": customer_code,
                            "item": item,
                            "batch_no": batch_no,
                            "org_code": org_code,
                            "bin_code": bin_code,
                            "sub_inventory": sub_inventory,
                            "qty":qty,
                            "process_flag": process_flag,
                            "error_desc": error_desc,
                            "picked_list_purpose":pick_list_purpose,
                            "delivery_note":delivery_note
                        })
                doc.insert()
                frappe.db.commit()
                return api_response(status=True,data=doc,message="Successfully Created Document",status_code=200)
            except Exception as e:
                    frappe.db.rollback()
                    return api_response(status=False,data='',message="Operation Failed",status_code=500)

            
            