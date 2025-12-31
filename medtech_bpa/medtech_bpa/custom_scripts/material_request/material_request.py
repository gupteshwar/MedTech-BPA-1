import frappe

def on_submit(doc, method):
    # Only MR created from RM button
    if not doc.get("custom_created_from_material_request_for_rm_button"):
        return

    try:
        # Get Sales Order safely
        if not doc.items or not doc.items[0].sales_order:
            frappe.throw("Sales Order not found in Material Request Items.")

        sales_order = doc.items[0].sales_order

        # -------------------------------
        # CREATE STOCK ENTRY
        # -------------------------------
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.stock_entry_type = "Material Transfer"
        stock_entry.purpose = "Material Transfer"
        stock_entry.company = doc.company
        stock_entry.reference_no = doc.name
        stock_entry.reference_type = "Material Request"

        has_items = False

        for item in doc.items:
            if (item.qty or 0) <= 0:
                continue

            stock_entry.append("items", {
                "item_code": item.item_code,
                "qty": item.qty,
                "uom": item.uom,
                "s_warehouse": item.from_warehouse,
                "t_warehouse": item.warehouse,
                "material_request": doc.name,
                "material_request_item": item.name,
                "fg_item_code": item.custom_fg_item_code or ""   # ✅ FG PASS
            })
            has_items = True

        if not has_items:
            frappe.throw("No quantity available to create Stock Entry.")

        stock_entry.insert(ignore_permissions=True)
        stock_entry.submit()

        # -----------------------------------
        # UPDATE SALES ORDER RM PENDING (FG SAFE)
        # -----------------------------------
        for se_item in stock_entry.items:

            fg_code = se_item.fg_item_code or ""

            # First try FG-wise row
            pending_row = frappe.db.get_value(
                "Sales Order RM Pending",
                {
                    "sales_order": sales_order,
                    "item_code": se_item.item_code,
                    "fg_item_code": fg_code,
                    "company": doc.company
                },
                ["name", "pending_qty"],
                as_dict=True
            )

            # Fallback → old records without FG
            if not pending_row:
                pending_row = frappe.db.get_value(
                    "Sales Order RM Pending",
                    {
                        "sales_order": sales_order,
                        "item_code": se_item.item_code,
                        "company": doc.company
                    },
                    ["name", "pending_qty"],
                    as_dict=True
                )

            if not pending_row or pending_row.pending_qty <= 0:
                continue

            issue_qty = min(se_item.qty, pending_row.pending_qty)

            frappe.db.sql("""
                UPDATE `tabSales Order RM Pending`
                SET
                    issued_qty = issued_qty + %s,
                    pending_qty = GREATEST(pending_qty - %s, 0)
                WHERE name = %s
            """, (
                issue_qty,
                issue_qty,
                pending_row.name
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
        frappe.throw("Failed to create Stock Entry. Please check Error Log.")
