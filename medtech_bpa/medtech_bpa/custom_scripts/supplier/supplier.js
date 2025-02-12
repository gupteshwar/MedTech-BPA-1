frappe.ui.form.on("Supplier", {
    onload: function (frm) {
        // Fetch the allow_manual_entry setting from Supplier Autoname Settings
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Supplier Autoname Settings",
                fieldname: "allow_manual_entry"
            },
            callback: function (response) {
                if (response.message) {
                    let allow_manual_entry = response.message.allow_manual_entry;

                    // Set the read-only property based on allow_manual_entry value
                    frm.set_df_property("custom_supplier_code_numeric", "read_only", !allow_manual_entry);
                }
            }
        });
    }
});
