import frappe
def on_submit(doc, method):

    # Only MR created from RM button
    if not doc.get("custom_created_from_material_request_for_rm_button"):
        return

    try:
        # Get Sales Order SAFELY
        sales_order = None
        if doc.items and doc.items[0].sales_order:
            sales_order = doc.items[0].sales_order
        else:
            frappe.throw("Sales Order not found in Material Request Items.")

        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.stock_entry_type = "Material Transfer"
        stock_entry.purpose = "Material Transfer"
        stock_entry.company = doc.company
        stock_entry.reference_no = doc.name
        stock_entry.reference_type = "Material Request"

        has_items = False

        for item in doc.items:
            if item.qty > 0:
                stock_entry.append("items", {
                    "item_code": item.item_code,
                    "qty": item.qty,
                    "uom": item.uom,
                    "s_warehouse": item.from_warehouse,
                    "t_warehouse": item.warehouse,
                    "material_request": doc.name,
                    "material_request_item": item.name
                })
                has_items = True

        if not has_items:
            frappe.throw("No quantity available to create Stock Entry.")

        stock_entry.insert(ignore_permissions=True)
        stock_entry.submit()

        # UPDATE SALES ORDER RM PENDING
        for se_item in stock_entry.items:
            frappe.db.sql("""
                UPDATE `tabSales Order RM Pending`
                SET
                    issued_qty = issued_qty + %s,
                    pending_qty = pending_qty - %s
                WHERE
                    sales_order = %s
                    AND item_code = %s
                    AND company = %s
            """, (
                se_item.qty,
                se_item.qty,
                sales_order,
                se_item.item_code,
                doc.company
            ))

        frappe.db.commit()

        frappe.msgprint(
            f"Stock Entry <b><a href='/app/stock-entry/{stock_entry.name}'>"
            f"{stock_entry.name}</a></b> created successfully."
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Stock Entry creation failed from Material Request"
        )
        frappe.throw("Failed to create Stock Entry.")