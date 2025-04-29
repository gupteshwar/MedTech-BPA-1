// Copyright (c) 2025, Indictrans and contributors
// For license information, please see license.txt

frappe.query_reports["BOM Rate Summary Report"] = {
	"filters": [
		{
            "fieldname": "bom",
            "label": "BOM",
            "fieldtype": "Link",
            "options": "BOM",
            "reqd": 0
        },
        {
            "fieldname": "item",
            "label": "Item",
            "fieldtype": "Link",
            "options": "Item",
            "reqd": 0
        },
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 0
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "reqd": 0
        }
    ]

	
};
