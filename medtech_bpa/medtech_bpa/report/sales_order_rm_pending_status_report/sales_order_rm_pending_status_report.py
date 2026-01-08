# Copyright (c) 2025, Indictrans and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Sales Order", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 140},
        {"label": "Order Type", "fieldname": "order_type", "fieldtype": "Data", "width": 120},

        {"label": "FG Item Code", "fieldname": "fg_item_code", "fieldtype": "Link", "options": "Item", "width": 130},
        {"label": "FG Item Name", "fieldname": "fg_item_name", "fieldtype": "Data", "width": 180},

        {"label": "Raw Material Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 140},
        {"label": "Raw Material Name", "fieldname": "raw_material_name", "fieldtype": "Data", "width": 200},

        {"label": "Required Qty", "fieldname": "required_qty", "fieldtype": "Float", "width": 110},
        {"label": "Issued Qty", "fieldname": "issued_qty", "fieldtype": "Float", "width": 110},
        {"label": "Pending Qty", "fieldname": "pending_qty", "fieldtype": "Float", "width": 110},

        {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 80},

        {"label": "Material Request No", "fieldname": "material_request", "fieldtype": "Link", "options": "Material Request", "width": 160},
        {"label": "Stock Entry No", "fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry", "width": 160},
    ]

def get_data(filters):
    conditions = []
    values = {}

    if filters.get("company"):
        conditions.append("so.company = %(company)s")
        values["company"] = filters["company"]

    if filters.get("sales_order"):
        conditions.append("so.sales_order = %(sales_order)s")
        values["sales_order"] = filters["sales_order"]

    if filters.get("order_type"):
        conditions.append("so.order_type = %(order_type)s")
        values["order_type"] = filters["order_type"]

    if filters.get("fg_item_code"):
        conditions.append("so.fg_item_code = %(fg_item_code)s")
        values["fg_item_code"] = filters["fg_item_code"]

    if filters.get("rm_item_code"):
        conditions.append("so.item_code = %(rm_item_code)s")
        values["rm_item_code"] = filters["rm_item_code"]

    if filters.get("pending_only"):
        conditions.append("so.pending_qty > 0")

    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = "WHERE " + where_clause

    query = f"""
        SELECT
            so.sales_order,
            so.order_type,
            so.fg_item_code,
            so.fg_item_name,
            so.item_code,
            so.raw_material_name,
            so.required_qty,
            so.issued_qty,
            so.pending_qty,
            so.uom,
            mr.parent AS material_request,
            se.parent AS stock_entry
        FROM `tabSales Order RM Pending` so
        LEFT JOIN (
            SELECT sales_order, item_code, parent
            FROM `tabMaterial Request Item`
            WHERE docstatus = 1
        ) mr ON mr.sales_order = so.sales_order AND mr.item_code = so.item_code
        LEFT JOIN (
            SELECT sed.item_code, sed.parent
            FROM `tabStock Entry Detail` sed
            JOIN `tabStock Entry` se ON sed.parent = se.name
            WHERE se.docstatus = 1
        ) se ON se.item_code = so.item_code
        {where_clause}
        ORDER BY so.sales_order, so.fg_item_code
    """

    return frappe.db.sql(query, values, as_dict=True)
