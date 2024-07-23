<<<<<<< HEAD
=======
import frappe
from ..api_utils.response import api_response
from datetime import datetime
@frappe.whitelist(allow_guest=False)
def create_quality_inspection(data):
    try:
        data = frappe.parse_json(data)
        
        #! Validate Purchase Receipt=========================================================================>
        purchase_receipt = data.get("purchase_receipt")
        if not purchase_receipt :
           return api_response(status_code=400, message="Purchase Receipt is required", data=[], status=False)
        if not frappe.db.exists("Purchase Receipt", purchase_receipt):
           return api_response(status_code=400, message="Purchase Receipt ID invalid", data=[], status=False)
        
        #! Validate required fields==========================================================================>
        inspected_by = data.get("inspected_by")
        if not inspected_by:
            return api_response(status_code=400, message="Inspector name is required", data=[], status=False)
        
        report_date = data.get("report_date")
        if not report_date:
            return api_response(status_code=400, message="Report date is required", data=[], status=False)
        
        item_code = data.get("item_code")

        if not item_code or not frappe.db.exists("Item", item_code):
            return api_response(status_code=400, message=f"{item_code} is not a valid item", data=[], status=False)

        billed_qty = data.get("billed_qty")
        billed_qty=int(billed_qty)
        if billed_qty is None or billed_qty < 0:
            return api_response(status_code=400, message=f"{billed_qty} is not a valid billed quantity", data=[], status=False)
        sample_size=data.get('sample_size')
        sample_size=float(sample_size)
        if sample_size is None or sample_size < 0:
            return api_response(status_code=400, message=f"{sample_size} is not a valid sample size", data=[], status=False)
        rejected_qty=data.get('rejected_qty')
        rejected_qty=int(rejected_qty)
        if rejected_qty is None or rejected_qty < 0:
            return api_response(status_code=400, message=f"{rejected_qty} is not a valid rejected quantity", data=[], status=False)
        branch=data.get('branch')
        if not branch:
            return api_response(status_code=400, message="Branch is required", data=[], status=False)
        status=data.get('status')
        if not status:
            return api_response(status_code=400, message="Status is required", data=[], status=False)
        batch_no=data.get('batch_no')
        qc_status=data.get('qc_status')

        #!if item is in Purchase Receipt
        
        
        purchase_receipt_in_items=frappe.db.get_all("Purchase Receipt Item",filters={
            "parent": purchase_receipt,
            "item_code":item_code},
        fields=["item_code","supplier_part_no","item_name","description",
                "uom","received_qty","qty","rejected_qty","serial_no",
                "serial_and_batch_bundle","rejected_serial_and_batch_bundle",
                "batch_no"
                ]
        )
        if len(purchase_receipt_in_items)==0:
            return api_response(status=False, data=[], 
                                message="Item  Doesn't Exists in Purchase Receipt/GRN/Visual Inspection Report", status_code=400) 

        
        #!quantity validation===============================================================================>
        purchase_item_qty=int(purchase_receipt_in_items[0].get("qty"))
        if billed_qty>purchase_item_qty:
            return api_response(status=False, data=[], 
                                message="Billed Quantity Exceeds Item Quantity in in Purchase Receipt/GRN/Visual Inspection Report", status_code=400)

        if sample_size>purchase_item_qty:
            return api_response(status=False, data=[], 
                                message="Sample Size Exceeds Item Quantity in Purchase Receipt", status_code=400)
        if rejected_qty>purchase_item_qty:
            return api_response(status=False, data=[], 
                                message="Rejected Quantity Exceeds Item Quantity in Purchase Receipt", status_code=400)
        if sample_size>billed_qty:
            return api_response(status=False, data=[], 
                                message="Billed / Rejected Quantity Less than Sample Size", status_code=400)
        if billed_qty + rejected_qty> purchase_item_qty:
            return api_response(status=False, data=[], 
                                message="Billed + Rejected Quantity Exceeds Purchase Receipt  Qty", status_code=400)

        #!==================================================================
        #!quantity left to confirm
        total_quality_inspection_item_quantity=0
        quality_inspection_item_quantity=frappe.db.get_all("Quality Inspection",
            filters={
            "inspection_type": "Incoming",
            "reference_type": "Purchase Receipt",
            "reference_name": purchase_receipt,
            "item_code": item_code},
            fields=["billed_qty","rejected_quantity"])
        
        for item in quality_inspection_item_quantity:
            total_quality_inspection_item_quantity+=int(item.get("billed_qty"))+int(item.get("rejected_quantity"))
        
        quantity_left_for_qc=purchase_item_qty-total_quality_inspection_item_quantity
        if billed_qty>quantity_left_for_qc:
            return api_response(status=False, data=[], 
                                message="Quantity left to confirm exceeds Item Quantity in Purchase Receipt", status_code=400)
        #!============================
        #!============================
        #!============================
        doc = frappe.get_doc({
            "doctype": "Quality Inspection",
            "inspection_type": "Incoming",
            "reference_type": "Purchase Receipt",
            "reference_name": purchase_receipt,
            "inspected_by": inspected_by,
            "report_date": report_date,
            "item_code": item_code,
            "branch": branch,
            "batch_no": batch_no,
            "sample_size": sample_size,
            "billed_qty":billed_qty,
            "rejected_quantity": rejected_qty,
            "qc_status":qc_status,
            "status":status})
        doc.insert()
        doc.submit()
        frappe.db.commit()
        #!============================
        #!============================
        #!============================
        return api_response(status_code=200, message="Quality Inspection Created Successfully", data=doc, status=True)
    except Exception as e:
        return api_response(status_code=400, message=f"Operation error {e}", data=[], status=False)
>>>>>>> ca0ea29 (api errors fixed and print format with signature and two digit after decimal added)
