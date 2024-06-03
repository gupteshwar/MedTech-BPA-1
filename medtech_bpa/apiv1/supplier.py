import frappe
from ..api_utils.response import api_response
from datetime import datetime

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
    customer_list = frappe.get_all("Supplier",
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
    if len(customer_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=customer_list, message="None", status_code=200)
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
        #return api_response(status=True, data=customer_list, message="None", status_code=200)
        
                        
   

