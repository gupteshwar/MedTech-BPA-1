frappe.ui.form.on("Supplier", {
    onload: function (frm) {
        console.log("Supplier form loaded"); // Log when the form loads

        // Fetch the allow_manual_entry setting from Supplier Autoname Settings
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Supplier Autoname Settings",
                fieldname: "allow_manual_entry"
            },
            callback: function (response) {
                console.log("Response from Supplier Autoname Settings:", response); // Log API response

                if (response && response.message) {
                    let allow_manual_entry = response.message.allow_manual_entry;
                    console.log("Allow Manual Entry Value:", allow_manual_entry); // Log the fetched value

                    // Ensure allow_manual_entry is a boolean (sometimes it may be returned as string or null)
                    allow_manual_entry = Boolean(Number(allow_manual_entry));

                    // Set the read-only property based on allow_manual_entry value
                    frm.set_df_property("custom_supplier_code", "read_only", !allow_manual_entry);
                    console.log("Updated field read-only property:", !allow_manual_entry);
                } else {
                    console.warn("No allow_manual_entry value found in response");
                }
            },
            error: function (err) {
                console.error("Error fetching Supplier Autoname Settings:", err);
            }
        });
    }
});
