import frappe

@frappe.whitelist()
def get_po_items_qty(po_name):
    if not po_name:
        return {"error": "Missing PO name"}
    po = frappe.get_doc("Purchase Order", po_name)
    total_qty_map = {item.item_code: item.qty for item in po.items}
    received_qty_map = {}
    purchase_receipt_items = frappe.db.get_all(
        "Purchase Receipt Item",
        filters={"purchase_order": po_name},
        fields=["item_code", "sum(qty) as received_qty", "parent"],
        group_by="item_code"
    )
    for item in purchase_receipt_items:
        docstatus = frappe.db.get_value("Purchase Receipt", item.parent, "docstatus")
        if docstatus in [0,1]:  
            received_qty_map[item.item_code] = received_qty_map.get(item.item_code, 0) + (item.received_qty or 0)

    qty_mapping = {}
    for item_code, total_qty in total_qty_map.items():
        received_qty = received_qty_map.get(item_code, 0)
        remaining_qty = total_qty - received_qty
        qty_mapping[item_code] = max(remaining_qty, 0) 

    return {
       
        "qty_mapping": qty_mapping
    }
