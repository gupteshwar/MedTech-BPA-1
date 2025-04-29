# Copyright (c) 2025, Indictrans and contributors
# For license information, please see license.txt

import frappe


import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    # Check if current user has "Hide Item Price" role
    user_roles = frappe.get_roles(frappe.session.user)
    if "Hide Item Price" in user_roles and "Administrator" not in user_roles:
        # Remove Rate and Amount columns
        columns = [col for col in columns if col['fieldname'] not in ['rate', 'amount']]

        # Also remove Rate and Amount fields from data
        for row in data:
            row.pop('rate', None)
            row.pop('amount', None)
    return columns, data
    


def get_columns():
    return [
        {"label": _("ID"), "fieldname": "bom", "fieldtype": "Link", "options": "BOM", "width": 200},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 80},
        {"label": _("Item"), "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": _("Is Default"), "fieldname": "is_default", "fieldtype": "Check", "width": 100},
        {"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 80},
        {"label": _("Item Code (BOM Item)"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": _("Item Name (BOM Item)"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": _("Qty (BOM Item)"), "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": _("Rate (BOM Item)"), "fieldname": "rate", "fieldtype": "Currency", "width": 100},
        {"label": _("Amount (BOM Item)"), "fieldname": "amount", "fieldtype": "Currency", "width": 100},
    ]

def get_conditions(filters):
    conditions = []
    if filters.get("bom"):
        conditions.append("bom.name = %(bom)s")
    if filters.get("item"):
        conditions.append("bom.item = %(item)s")
    if filters.get("company"):
        conditions.append("bom.company = %(company)s")
    if filters.get("from_date"):
        conditions.append("bom.creation >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("bom.creation <= %(to_date)s")
    return " AND " + " AND ".join(conditions) if conditions else ""

def get_data(filters):
    conditions = get_conditions(filters)
    data = frappe.db.sql("""
        SELECT 
            bom.name as bom,
            bom.is_active,
            bom.is_default,
            bom.item as item,
            bom.is_default,
            bom.currency,
            bi.item_code,
            bi.item_name,
            bi.qty,
            bi.rate,
            bi.amount
        FROM
            `tabBOM` bom
        INNER JOIN
            `tabBOM Item` bi ON bi.parent = bom.name
        WHERE
            bom.docstatus < 2 {conditions}
        ORDER BY
            bom.name
    """.format(conditions=conditions), filters, as_dict=1)
    for row in data:
        if row.get("is_active") == 1 and row.get("is_default") == 1:
            row["status"] = "Default"
        elif row.get("is_active") == 1 and row.get("is_default") == 0:
            row["status"] = "Active"
        else:
            row["status"] = "Not Active"
    return data
