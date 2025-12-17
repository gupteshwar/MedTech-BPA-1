# Copyright (c) 2025, Indictrans and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, flt, cint, get_datetime
from erpnext.stock.utils import get_incoming_rate


def execute(filters=None):
	if not filters:
		filters = {}

	validate_filters(filters)

	columns = get_columns(filters)
	data = get_stock_ledger_entries(filters)

	return columns, data


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("Company is mandatory"))

	if not filters.get("from_date") or not filters.get("to_date"):
		frappe.throw(_("From Date and To Date are mandatory"))


def get_columns(filters):
	columns = [
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 140,
		},
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 150},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120,
		},
		{"label": _("Item Name"), "fieldname": "item_name", "width": 140},
		{
			"label": _("Stock UOM"),
			"fieldname": "stock_uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 90,
		},
		{"label": _("In Qty"), "fieldname": "in_qty", "fieldtype": "Float", "width": 90},
		{"label": _("Out Qty"), "fieldname": "out_qty", "fieldtype": "Float", "width": 90},
		{"label": _("Balance Qty"), "fieldname": "qty_after_transaction", "fieldtype": "Float", "width": 110},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 160,
		},
		{"label": _("Item Group"), "fieldname": "item_group", "width": 120},
		{"label": _("Brand"), "fieldname": "brand", "width": 100},
		{"label": _("Description"), "fieldname": "description", "width": 200},
		{"label": _("Incoming Rate"), "fieldname": "incoming_rate", "fieldtype": "Float", "width": 110},
		{"label": _("Valuation Rate"), "fieldname": "valuation_rate", "fieldtype": "Float", "width": 110},
		{"label": _("Balance Value"), "fieldname": "stock_value", "fieldtype": "Currency", "width": 120},
		{"label": _("Value Change"), "fieldname": "stock_value_difference", "fieldtype": "Currency", "width": 120},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 120},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 140,
		},
		{"label": _("Batch"), "fieldname": "batch_no", "width": 120},
		{"label": _("Serial No"), "fieldname": "serial_no", "width": 160},
		{"label": _("Project"), "fieldname": "project", "width": 120},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 120,
		},
	]

	return columns


def get_stock_ledger_entries(filters):
	from_date = get_datetime(filters["from_date"] + " 00:00:00")
	to_date = get_datetime(filters["to_date"] + " 23:59:59")

	sle = frappe.qb.DocType("Stock Ledger Entry")
	item = frappe.qb.DocType("Item")
	se = frappe.qb.DocType("Stock Entry")
	sed = frappe.qb.DocType("Stock Entry Detail")
	mri = frappe.qb.DocType("Material Request Item")
	mr = frappe.qb.DocType("Material Request")

	query = (
		frappe.qb.from_(sle)
		.left_join(item).on(item.name == sle.item_code)
		.left_join(se).on(
			(se.name == sle.voucher_no) & (sle.voucher_type == "Stock Entry")
		)
		.left_join(sed).on(
			(sed.parent == se.name) & (sed.item_code == sle.item_code)
		)
		.left_join(mri).on(mri.name == sed.material_request_item)
		.left_join(mr).on(mr.name == mri.parent)
		.select(
			sle.posting_datetime.as_("date"),
			sle.item_code,
			item.item_name,
			item.stock_uom,
			item.item_group,
			item.brand,
			item.description,
			sle.warehouse,
			sle.actual_qty,
			sle.qty_after_transaction,
			sle.incoming_rate,
			sle.valuation_rate,
			sle.stock_value,
			sle.stock_value_difference,
			sle.voucher_type,
			sle.voucher_no,
			sle.batch_no,
			sle.serial_no,
			sle.project,
			sle.company,
			mri.sales_order.as_("sales_order"),
		)
		.where(
			(sle.docstatus < 2)
			& (sle.is_cancelled == 0)
			& (sle.company == filters["company"])
			& (sle.posting_datetime[from_date:to_date])
		)
		.orderby(sle.posting_datetime)
		.orderby(sle.creation)
	)

	if filters.get("warehouse"):
		query = query.where(sle.warehouse == filters.get("warehouse"))

	if filters.get("item_code"):
		query = query.where(sle.item_code == filters.get("item_code"))

	data = query.run(as_dict=True)

	for d in data:
		d["in_qty"] = flt(d.actual_qty) if flt(d.actual_qty) > 0 else 0
		d["out_qty"] = abs(flt(d.actual_qty)) if flt(d.actual_qty) < 0 else 0

	return data