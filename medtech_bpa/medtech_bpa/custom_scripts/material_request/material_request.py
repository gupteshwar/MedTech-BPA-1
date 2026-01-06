import frappe

def on_submit(doc, method):
    # Only MR created from RM button
    if not doc.get("custom_created_from_material_request_for_rm_button"):
        return

    try:
        if not doc.items or not doc.items[0].sales_order:
            frappe.throw("Sales Order not found in Material Request.")

        sales_order = doc.items[0].sales_order

        # CREATE STOCK ENTRY
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
                "custom_fg_item_code": item.custom_fg_item_code,
                "custom_so_item_row_id": item.custom_so_item_row_id
            })
            has_items = True

        if not has_items:
            frappe.throw("No quantity available to create Stock Entry.")

        stock_entry.insert(ignore_permissions=True)
        stock_entry.submit()

        # -------------------------------
        # UPDATE SALES ORDER RM PENDING
        # -------------------------------
        for se_item in stock_entry.items:

            issue_qty = se_item.qty or 0
            if issue_qty <= 0:
                continue

            child_row = frappe.db.get_value(
                "Sales Order RM Pending Item",
                {
                    "parenttype": "Sales Order RM Pending",
                    "raw_material": se_item.item_code,
                    "parent": frappe.db.get_value(
                        "Sales Order RM Pending",
                        {
                            "sales_order": sales_order,
                            "fg_item_code": se_item.custom_fg_item_code,
                            "so_item_row_id": se_item.custom_so_item_row_id,
                            "company": doc.company
                        },
                        "name"
                    )
                },
                ["name", "pending_qty", "issued_qty"],
                as_dict=True
            )

            if not child_row or child_row.pending_qty <= 0:
                continue

            actual_issue = min(issue_qty, child_row.pending_qty)

            frappe.db.sql("""
                UPDATE `tabSales Order RM Pending Item`
                SET
                    issued_qty = issued_qty + %s,
                    pending_qty = pending_qty - %s
                WHERE name = %s
            """, (actual_issue, actual_issue, child_row.name))
        frappe.db.commit()

        frappe.msgprint(
            f"Stock Entry <b><a href='/app/stock-entry/{stock_entry.name}'>"
            f"{stock_entry.name}</a></b> created successfully."
        )

    except Exception:
        frappe.log_error(frappe.get_traceback(), "MR Submit Failed")
        frappe.throw("Failed to submit Material Request.")


def on_cancel(doc, method):
    # Only MR created from RM button
    if not doc.get("custom_created_from_material_request_for_rm_button"):
        return

    try:
        # Safety: Sales Order must exist
        if not doc.items or not doc.items[0].sales_order:
            return

        sales_order = doc.items[0].sales_order

        for item in doc.items:

            if (item.qty or 0) <= 0:
                continue

            fg_code = item.custom_fg_item_code or ""
            so_row_id = item.custom_so_item_row_id or ""

            # Find parent RM Pending doc
            parent_name = frappe.db.get_value(
                "Sales Order RM Pending",
                {
                    "sales_order": sales_order,
                    "fg_item_code": fg_code,
                    "so_item_row_id": so_row_id,
                    "company": doc.company
                },
                "name"
            )

            if not parent_name:
                continue

            # Find child RM Pending Item
            child_row = frappe.db.get_value(
                "Sales Order RM Pending Item",
                {
                    "parent": parent_name,
                    "raw_material": item.item_code
                },
                ["name", "issued_qty"],
                as_dict=True
            )

            if not child_row or (child_row.issued_qty or 0) <= 0:
                continue

            revert_qty = min(item.qty, child_row.issued_qty)

            if revert_qty <= 0:
                continue

            # Revert quantities
            frappe.db.sql("""
                UPDATE `tabSales Order RM Pending Item`
                SET
                    issued_qty = issued_qty - %s,
                    pending_qty = pending_qty + %s
                WHERE name = %s
            """, (
                revert_qty,
                revert_qty,
                child_row.name
            ))

        frappe.db.commit()

        frappe.msgprint(
            "Sales Order RM Pending quantities reverted successfully."
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "RM Pending revert failed on MR Cancel"
        )
        frappe.throw("Failed to revert RM Pending on Material Request cancel.")