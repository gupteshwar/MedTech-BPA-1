import frappe
from ..api_utils.response import api_response
from datetime import datetime
@frappe.whitelist(allow_guest=False)
def create_quality_inspection(data):
    # try:
    #     data = frappe.parse_json(data)
        
        # Validate Purchase Receipt
        purchase_receipt = data.get("purchase_receipt")
        if not purchase_receipt or not frappe.db.exists("Purchase Receipt", purchase_receipt):
           return api_response(status_code=400, message="Purchase Receipt is required", data=[], status=False)
        
        # Validate required fields
        inspected_by = data.get("inspected_by")
        if not inspected_by:
            return api_response(status_code=400, message="Inspector name is required", data=[], status=False)
        
        inspection_date = data.get("inspection_date")
        if not inspection_date:
            return api_response(status_code=400, message="Inspection date is required", data=[], status=False)
        
        submission_date = data.get("submission_date")
        if not submission_date:
            return api_response(status_code=400, message="Submission date is required", data=[], status=False)
        
        # Validate items
        items = data.get("items", [])
        if not items:
            return {"status": "error", "message": _("No items provided")}
        
        valid_items = []
        for item in items:
            item_code = item.get("item_code")
            qty = item.get("qty")
            billed_qty = item.get("billed_qty")
            rejected_qty = item.get("rejected_qty")
            accepted_qty = item.get("accepted_qty")
            warehouse = item.get("warehouse")
            batch_no = item.get("batch_no")  # Optional batch number
            readings = item.get("readings", [])
            
            if not item_code or not frappe.db.exists("Item", item_code):
                return api_response(status_code=400, message=f"{item_code} is not a valid item", data=[], status=False)
            
            if qty is None or qty < 0:
                return api_response(status_code=400, message=f"{qty} is not a valid quantity", data=[], status=False)
            
            if billed_qty is None or billed_qty < 0:
                return api_response(status_code=400, message=f"{billed_qty} is not a valid billed quantity", data=[], status=False)
            
            if rejected_qty is None or rejected_qty < 0:
                return api_response(status_code=400, message=f"{rejected_qty} is not a valid rejected quantity", data=[], status=False)
            
            if accepted_qty is None or accepted_qty < 0:
                return api_response(status_code=400, message=f"{accepted_qty} is not a valid accepted quantity", data=[], status=False)
            
            if not warehouse or not frappe.db.exists("Warehouse", warehouse):
                return api_response(status_code=400, message=f"{warehouse} is not a valid warehouse", data=[], status=False)
            
            valid_item = {
                "item_code": item_code,
                "qty": qty,
                "billed_qty": billed_qty,
                "rejected_qty": rejected_qty,
                "accepted_qty": accepted_qty,
                "warehouse": warehouse,
                "readings": []
            }
            
            if batch_no:
                valid_item["batch_no"] = batch_no
            
            for reading in readings:
                parameter = reading.get("parameter")
                value = reading.get("value")
                if parameter and value is not None:
                    valid_item["readings"].append({
                        "parameter": parameter,
                        "value": value
                    })
            
            valid_items.append(valid_item)
        
        # Create the Quality Inspection document
        doc = frappe.get_doc({
            "doctype": "Quality Inspection",
            "inspection_type": "Incoming",
            "reference_type": "Purchase Receipt",
            "reference_name": purchase_receipt,
            "inspected_by": inspected_by,
            "inspection_date": inspection_date,
            "submission_date": submission_date,
            "items": valid_items,
            "status": "Submitted"
        })
        doc.insert()
        doc.submit()
        frappe.db.commit()
        
        return api_response(status_code=200, message="Quality Inspection Created Successfully", data=doc, status=True)
    # except Exception as e:
    #     return api_response(status_code=400, message=f"Operation error {e}", data=[], status=False)
