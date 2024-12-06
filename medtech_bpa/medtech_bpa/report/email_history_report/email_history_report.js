frappe.query_reports["Email History Report"] = {
    "filters": [
        {
            "fieldname": "sender",
            "label": __("Sender"),
            "fieldtype": "Data",
            "default": ""
        },
        {
            "fieldname": "reference_doctype",
            "label": __("Reference Doctype"),
            "fieldtype": "Data",
            "default": ""
        }
    ]
};
