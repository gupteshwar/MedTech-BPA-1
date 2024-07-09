import frappe
from ..api_utils.response import api_response
from datetime import datetime
from bs4 import BeautifulSoup

@frappe.whitelist(allow_guest=False,methods=["GET"])
def getSupplierList(timestamp="",limit=50,offset=0):

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
    #!======================================
    supplier_list = frappe.get_all("Supplier",
        fields=["supplier_name as supplier_name",
                "country as supplier_country",
                "supplier_group as supplier_group",
                "tax_id as supplier_tax_id",
                "mobile_no",
                "email_id",
                "supplier_primary_contact as supplier_contact",
                "primary_address",
                "modified as updated_at"
                ],
            
            filters={
                'modified':['>',timestamp]
            },
            limit=limit,
            start=offset,
            order_by='-modified'
        )
   
    #!alter long string text
    for supplier in supplier_list:
        if supplier.primary_address:
            soup = BeautifulSoup(supplier.primary_address, 'html.parser')
            supplier.primary_address = soup.get_text()
    #!================================================================
    supplier_list_timestamp=frappe.get_all("Supplier",filters={'modified':['>',timestamp]})
    data_size=len(supplier_list_timestamp)
    #!================================================================
    if len(supplier_list)==0:
        return api_response(status=True,data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, 
                            data=supplier_list, 
                            message="None", 
                            status_code=200,
                            data_size=data_size)
        
                        
   

