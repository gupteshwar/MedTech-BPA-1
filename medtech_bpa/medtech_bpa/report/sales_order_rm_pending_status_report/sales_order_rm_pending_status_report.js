// Copyright (c) 2025, Indictrans and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order RM Pending Status Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname: "sales_order",
			label: __("Sales Order"),
			fieldtype: "Link",
			options: "Sales Order"
		},
		{
			fieldname: "fg_item_code",
			label: __("FG Item"),
			fieldtype: "Link",
			options: "Item"
		},
		{
			fieldname: "rm_item_code",
			label: __("Raw Material"),
			fieldtype: "Link",
			options: "Item"
		}
	]
};
