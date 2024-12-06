frappe.query_reports["Customer Email Contact Report"] = {
    "filters": [
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "reqd": 0
        },
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "reqd": 0
        },
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "reqd": 0
        }
    ],

    // Custom logic to execute when the report is loaded or refreshed
    "onload": function(report) {
        frappe.msgprint(__('Welcome to the Customer Email Contact Report!'));
    },

    // Custom behavior before the report is refreshed
    "before_query": function(filters) {
        console.log("Filters applied:", filters);
    }
};
