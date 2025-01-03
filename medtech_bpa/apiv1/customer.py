import frappe
from ..api_utils.response import api_response
from datetime import datetime
from bs4 import BeautifulSoup

#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getCustomerList(timestamp="",limit=50,offset=0):

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

   
    customer_list = frappe.get_all("Customer",
        fields=["customer_code as customer_code",
                "customer_name as customer_name",
                "customer_type",
                "customer_group",
                "tax_id",
                "territory",
                "mobile_no",
                "email_id",
                "customer_primary_contact",
                "customer_primary_address",
                "primary_address",
                "modified as updated_at",
                
                ],
            
            filters={
                'modified':['>',timestamp]
            },
            limit=limit,
            start=offset,
            order_by='-modified'
        )
    #!alter long string text
    for customer in customer_list:
        if customer.primary_address:
            soup = BeautifulSoup(customer.primary_address, 'html.parser')
            customer.primary_address = soup.get_text()
    #!total length without the timestamp filter 
    #!=============================================================================================
    customer_total_before_timestamp= frappe.get_all("Customer")
    data_size_before_timestamp=len(customer_total_before_timestamp)
    #!=============================================================================================

                        
    #!total length with the timestamp filter 
    #!=============================================================================================
    customer_total_after_timestamp= frappe.get_all("Customer",filters={'modified':['>',timestamp]})
    data_size=len(customer_total_after_timestamp)
    #!total length with the timestamp filter 
    #!=============================================================================================
    customer_total_after_timestamp= frappe.get_all("Customer",filters={'modified':['>',timestamp]})
    data_size=len(customer_total_after_timestamp)
    #!=============================================================================================
    if len(customer_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=customer_list, message="Successfully Fetched All Customers", status_code=200,data_size=data_size)
    
        
                        
   

#!----------------------------------------------------------------------------------------
#!COMMIT
