import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getCustomerList(timestamp="",limit=50,offset=0):

    #!limit offset int format check
    try:
        limit = int(limit)
        offset = int(offset)
    except:
        return api_response(status=False, data=[], message="Please Enter Proper Limit and Offset", status_code=400)
    #!limit and offset upper limit validation
    if limit > 500 or limit < 0 or offset<0:
        return api_response(status=False, data=[], message="Limit exceeded 500", status_code=400)
    #!timestamp non empty validation
    if timestamp is None or timestamp =="":
        return api_response(status=False, data=[], message="Please Enter a timestamp", status_code=400)
    #!timestamp format validation
    try:
        timestamp_datetime=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print("timestamp format validation failed\n\n" ,e)
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
                "modified"
                ],
            
            filters={
                'modified':['>',timestamp]
            },
            limit=limit,
            start=offset,
            order_by='-modified'
        )
    if len(customer_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        # for customer in customer_list:
        #     address=customer.get("customer_primary_address")
        #     if address is not None and address!="":
        #         #!get customer_details
        #         customer_address=frappe.db.get_all("Address",filters={"name":address},
        #                                            fields=["address_line1",
        #                                                    "address_line2",
        #                                                    "city",
        #                                                    "county",
        #                                                    "state",
        #                                                    "address_type",
        #                                                    "pincode"
        #                                                    ])
        #         if len(customer_address)>0:
        #             customer_address=customer_address[0]
        #             address_line1=customer_address.get("address_line1")
        #             address_line2=customer_address.get("address_line1")
        #             city=customer_address.get("city")
        #             country=customer_address.get("country")
        #             state=customer_address.get("state")
        #             address_type=customer_address.get("address_type")
        #             picode=customer_address.get("picode")
        #             customer["customer_address"]={
        #                 "address_line1":address_line1,
        #                 "address_line2":address_line2,
        #                 "city":city,
        #                 "country":country,
        #                 "state":state,
        #                 "address_type":address_type,
        #                 "pincode":picode,
        #             }
        #         else:
        #             customer["customer_address"]={
        #                 "address_line1":"",
        #                 "address_line2":"",
        #                 "city":"",
        #                 "country":"",
        #                 "state":"",
        #                 "address_type":"",
        #                 "pincode":"",
        #             }
        return api_response(status=True, data=customer_list, message="None", status_code=200)
        
                        
   

