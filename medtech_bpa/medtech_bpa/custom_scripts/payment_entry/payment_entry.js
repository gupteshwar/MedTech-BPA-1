
frappe.ui.form.on("Payment Entry", {


	refresh: function(frm){

		if(frm.doc.party_type == "Customer"
			&& (!frm.doc.payment_allocation_status ||
			in_list(["Pending", "Partially Allocated"], frm.doc.payment_allocation_status))
			&& frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Stock Allocation'), function () {
				frm.trigger("redirect_to_stock_allocation");
			}).addClass("btn-primary");;
		}
		//
		

	},
	bank_account: function(frm){
		
		if(frm.doc.payment_type=="Pay" && frm.doc.party_type!=null && frm.doc.party!=null){
			frappe.db.get_value("Bank Account",{"name": frm.doc.bank_account},"account",(r)=>{
				frm.set_value("paid_from",r.account)
			})

		}
	},
	
	redirect_to_stock_allocation: function(frm) {
		frappe.route_options = {
			"stock_allocation_party": frm.doc.party,
			"unallocated_amt": frm.doc.unallocated_amount,
			"posting_date": frm.doc.posting_date,
			"payment_entry": frm.doc.name
		};
		frappe.set_route("so_stock_allocation");
	},
	


	before_save: function (frm) {
        // Set Paid Amount to Total Allocated Amount before saving
		frm.doc.paid_amount = frm.doc.total_allocated_amount;
    }
});

