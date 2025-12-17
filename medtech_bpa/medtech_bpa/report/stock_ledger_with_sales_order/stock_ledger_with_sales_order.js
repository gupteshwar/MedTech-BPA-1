// Copyright (c) 2025, Indictrans and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Ledger with Sales Order"] = {
    filters: [
        {
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "item_code",
            label: __("Item"),
            fieldtype: "Link",
            options: "Item"
        },
        {
            fieldname: "warehouse",
            label: __("Warehouse"),
            fieldtype: "Link",
            options: "Warehouse"
        }
    ],

    onload: function(report) {
        // Optional: automatically refresh on load
        report.page.set_title(__("Stock Ledger with Sales Order"));
    },

    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "voucher_no" && data.voucher_type) {
            value = `<a href="/app/${data.voucher_type}/${data.voucher_no}" target="_blank">${value}</a>`;
        }

        if (column.fieldname === "sales_order" && data.sales_order) {
            value = `<a href="/app/Sales Order/${data.sales_order}" target="_blank">${value}</a>`;
        }

        return value;
    }
};
