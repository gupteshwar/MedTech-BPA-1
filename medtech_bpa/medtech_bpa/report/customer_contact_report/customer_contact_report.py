import frappe
def execute(filters=None):
    # Fetch columns and data
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    # Define the columns for the report
    return [
        {"label": "Customer", "fieldname": "linked_customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Email ID", "fieldname": "email_id", "fieldtype": "Data", "width": 200},
        {"label": "Contact Name", "fieldname": "name", "fieldtype": "Data", "width": 150},
        {"label": "Phone", "fieldname": "phone", "fieldtype": "Data", "width": 120},
        
    ]

def get_data(filters):
    # Apply filters if any
    conditions = ""
    if filters.get("customer"):
        conditions += " AND link.link_name = %(customer)s"
    if filters.get("supplier"):
        conditions += " AND link.link_name = %(supplier)s"
    if filters.get("employee"):
        conditions += " AND link.link_name = %(employee)s"

    # Fetch data from Contact and Dynamic Link doctypes
    query = f"""
        SELECT
            contact.name,
            contact.email_id,
            contact.phone,
            CASE
                WHEN link.link_doctype = 'Customer' THEN link.link_name
                ELSE NULL
            END AS linked_customer,
            CASE
                WHEN link.link_doctype = 'Supplier' THEN link.link_name
                ELSE NULL
            END AS linked_supplier,
            CASE
                WHEN link.link_doctype = 'Employee' THEN link.link_name
                ELSE NULL
            END AS linked_employee
        FROM
            `tabContact` contact
        LEFT JOIN
            `tabDynamic Link` link
        ON
            contact.name = link.parent
        WHERE
            link.parenttype = 'Contact'
            {conditions}
    """
    return frappe.db.sql(query, filters, as_dict=True)
