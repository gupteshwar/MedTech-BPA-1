import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"fieldname": "sender", "label": "Sender", "fieldtype": "Data", "width": 200},
        {"fieldname": "recipient", "label": "Recipient", "fieldtype": "Data", "width": 200},
        {"fieldname": "reference_doctype", "label": "Reference Doctype", "fieldtype": "Data", "width": 150},
        {"fieldname": "reference_name", "label": "Reference Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "party", "label": "Party (Customer/Supplier)", "fieldtype": "Data", "width": 200},
        {"fieldname": "eq_status", "label": "Email Queue Status", "fieldtype": "Data", "width": 120},
        {"fieldname": "eqr_status", "label": "Recipient Status", "fieldtype": "Data", "width": 120}
    ]

    conditions = []
    values = {}

    # If you want to enable filtering by sender or reference_doctype, uncomment and use filters.
    # if filters.get("sender"):
    #     conditions.append("eq.sender = %(sender)s")
    #     values["sender"] = filters["sender"]

    # if filters.get("reference_doctype"):
    #     conditions.append("eq.reference_doctype = %(reference_doctype)s")
    #     values["reference_doctype"] = filters["reference_doctype"]

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # Joining with relevant doctypes to fetch customer or supplier
    # For Sales Invoice (si_table), Sales Order (so_table), Delivery Note (dn_table): Use customer
    # For Purchase Order (po_table): Use supplier
    data = frappe.db.sql(f"""
        SELECT
            eq.sender,
            eqr.recipient,
            eq.reference_doctype,
            eq.reference_name,
            CASE
                WHEN eq.reference_doctype = 'Purchase Order' THEN po_table.supplier
                WHEN eq.reference_doctype = 'Sales Invoice' THEN si_table.customer
                WHEN eq.reference_doctype = 'Sales Order' THEN so_table.customer
                WHEN eq.reference_doctype = 'Delivery Note' THEN dn_table.customer
                ELSE NULL
            END AS party,
            eq.status AS eq_status,
            eqr.status AS eqr_status
        FROM `tabEmail Queue` eq
        LEFT JOIN `tabEmail Queue Recipient` eqr ON eq.name = eqr.parent

        -- Sales-related joins
        LEFT JOIN `tabSales Invoice` si_table
            ON eq.reference_doctype = 'Sales Invoice' AND eq.reference_name = si_table.name
        LEFT JOIN `tabSales Order` so_table
            ON eq.reference_doctype = 'Sales Order' AND eq.reference_name = so_table.name
        LEFT JOIN `tabDelivery Note` dn_table
            ON eq.reference_doctype = 'Delivery Note' AND eq.reference_name = dn_table.name

        -- Purchase-related join
        LEFT JOIN `tabPurchase Order` po_table
            ON eq.reference_doctype = 'Purchase Order' AND eq.reference_name = po_table.name

        {where_clause}
    """, values=values, as_dict=True)

    return columns, data
