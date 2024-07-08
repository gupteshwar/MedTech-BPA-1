# import frappe
# from ..api_utils.response import api_response
# from datetime import datetime
# from bs4 import BeautifulSoup

# #!Paginated Get Customer Details API
# @frappe.whitelist(allow_guest=False,methods=["GET"])
# def getItemGroupList(timestamp="",limit=100,offset=0):

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

#     item_group_list = frappe.get_all("Item Group",
#         fields=["item_group_name as item_group_name",
#                 "parent_item_group as parent_item_group",
#                 "is_group as is_group",
#                 "modified as updated_at"
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
       
        
                        
   



# @frappe.whitelist(allow_guest=False,methods=["GET"])
# def getItemList(timestamp="",limit=100,offset=0):

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

#     item_list = frappe.get_all("Item",
#         fields=["item_group as item_category_name",
#                 "item_name as item_name",
#                 "item_code as item_code",
#                 "description as item_description",
#                 "stock_uom as item_stock_uom",
#                 "modified as updated_at",
#                 "weight_per_unit",
#                 "weight_uom",
#                 "name as id"
#                 ],
            
#             filters={
#                 'modified':['>',timestamp]
#             },
#             limit=limit,
#             start=offset,
#             order_by='-modified'
#         )
#     #!==========================================================================================
#     for item in item_list:
#          if item.item_description:
#             soup = BeautifulSoup(item.item_description, 'html.parser')
#             item.item_description = soup.get_text()

#     #!==========================================================================================
#     item_list_with_timestamp = frappe.get_all("Item",
       
            
#             filters={
#                 'modified':['>',timestamp]
#             },
#         )
#     data_size=len(item_list_with_timestamp)
#     #!==============================================================================================
#     if len(item_list)==0:
#         return api_response(status=True, data=[], message="Empty Content", status_code=204)
#     else:
#         for item in item_list:
#             item_barcode_list=frappe.db.get_all("Item Barcode",filters={"parent":item["id"]},fields=["barcode_type"])
#             item["barcode"]=item_barcode_list
#         return api_response(status=True, 
#                             data=item_list, 
#                             message="Successfully Fetched Items", 
#                             status_code=200,
#                             data_size=data_size)

       
        
                        