// Copyright (c) 2016, Indictrans and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Tracker Report"] = {
	"filters": [
		{
			"label": __("VIR From Date"),
			"fieldname":"from_date",
			"fieldtype": "Date"
		},
		{
			"label": __("VIR To Date"),
			"fieldname":"to_date",
			"fieldtype": "Date"
		},
		//added po date filter
		{
			"label": __("PO From Date"),
			"fieldname":"po_from_date",
			"fieldtype": "Date"
		},
		{
			"label": __("PO To Date"),
			"fieldname":"po_to_date",
			"fieldtype": "Date"
		},
		{
			"label": __("Items"),
			"fieldname":"items",
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Item', txt);
			}
		},
		{
			"label": __("PO No"),
			"fieldname":"po_no",
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Purchase Order', txt);
			}		
		}	
	]
};
