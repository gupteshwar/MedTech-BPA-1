import frappe
# method to create SE only if MR is created from Custom Button Material For RM
def on_submit(doc,method):
        try:
            # Check for duplicate Stock Entry
            # existing_entry = frappe.db.exists("Stock Entry Detail", {
            #     "material_request": doc.name,
            # })
            # if existing_entry:
            #     frappe.msgprint(f"Stock Entry already exists")
            #     return

            # Create new Stock Entry
            if doc.get("custom_created_from_material_request_for_rm_button"):
                stock_entry = frappe.new_doc("Stock Entry")
                stock_entry.stock_entry_type = "Material Transfer"
                stock_entry.purpose = "Material Transfer"
                stock_entry.company = doc.company
                stock_entry.reference_no = doc.name
                stock_entry.reference_type = "Material Request"

                for item in doc.items:
                    if not item.item_code or not item.qty:
                        continue
                    stock_entry.append("items", {
                        "item_code": item.item_code,
                        "qty": item.qty,
                        "uom": item.uom,
                        "s_warehouse": item.from_warehouse,
                        "t_warehouse": item.warehouse,
                        "material_request":doc.name,
                        "material_request_item":item.name
                    })

                stock_entry.insert(ignore_permissions=True)
                frappe.msgprint(f"Stock Entry <b><a href='/app/stock-entry/{stock_entry.name}'>{stock_entry.name}</a></b> has been created")

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Stock Entry creation failed")
            frappe.throw(f"Failed to create Stock Entry")