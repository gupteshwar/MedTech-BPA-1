# import frappe
# from ..api_utils.response import api_response
# from datetime import datetime
# @frappe.whitelist(allow_guest=False)
# def create_quality_inspection(data):
#     try:
#         data = frappe.parse_json(data)
        
#         # Validate Purchase Receipt
#         purchase_receipt = data.get("purchase_receipt")
#         if not purchase_receipt :
#            return api_response(status_code=400, message="Purchase Receipt is required", data=[], status=False)
#         if not frappe.db.exists("Purchase Receipt", purchase_receipt):
#            return api_response(status_code=400, message="Purchase Receipt ID invalid", data=[], status=False)
        
#         # Validate required fields
#         inspected_by = data.get("inspected_by")
#         if not inspected_by:
#             return api_response(status_code=400, message="Inspector name is required", data=[], status=False)
        
#         report_date = data.get("report_date")
#         if not report_date:
#             return api_response(status_code=400, message="Report date is required", data=[], status=False)
        
#         item_code = data.get("item_code")

#         if not item_code or not frappe.db.exists("Item", item_code):
#             return api_response(status_code=400, message=f"{item_code} is not a valid item", data=[], status=False)

#         billed_qty = data.get("billed_qty")
#         billed_qty=int(billed_qty)
#         if billed_qty is None or billed_qty < 0:
#             return api_response(status_code=400, message=f"{billed_qty} is not a valid billed quantity", data=[], status=False)
#         sample_size=data.get('sample_size')
#         sample_size=float(sample_size)
#         if sample_size is None or sample_size < 0:
#             return api_response(status_code=400, message=f"{sample_size} is not a valid sample size", data=[], status=False)
#         rejected_qty=data.get('rejected_qty')
#         rejected_qty=int(rejected_qty)
#         if rejected_qty is None or rejected_qty < 0:
#             return api_response(status_code=400, message=f"{rejected_qty} is not a valid rejected quantity", data=[], status=False)
#         branch=data.get('branch')
#         if not branch:
#             return api_response(status_code=400, message="Branch is required", data=[], status=False)
#         status=data.get('status')
#         if not status:
#             return api_response(status_code=400, message="Status is required", data=[], status=False)
#         batch_no=data.get('batch_no')
#         qc_status=data.get('qc_status')
#         doc = frappe.get_doc({
#             "doctype": "Quality Inspection",
#             "inspection_type": "Incoming",
#             "reference_type": "Purchase Receipt",
#             "reference_name": purchase_receipt,
#             "inspected_by": inspected_by,
#             "report_date": report_date,
#             "item_code": item_code,
#             "branch": branch,
#             "batch_no": batch_no,
#             "sample_size": sample_size,
#             "billed_qty":billed_qty,
#             "rejected_quantity": rejected_qty,
#             "qc_status":qc_status,
#             "status":status})

            
        
#         doc.insert()
#         doc.submit()
#         frappe.db.commit()
        
#         return api_response(status_code=200, message="Quality Inspection Created Successfully", data=doc, status=True)
#     except Exception as e:
#         return api_response(status_code=400, message=f"Operation error {e}", data=[], status=False)
