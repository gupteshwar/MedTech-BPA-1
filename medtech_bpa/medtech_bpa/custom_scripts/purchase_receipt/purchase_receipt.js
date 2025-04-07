
frappe.ui.form.on("Purchase Receipt", {
	onload: function(frm){	
		if(cur_frm.doc.__islocal == 1 && cur_frm.doc.is_return == 1){
			if(frm.doc.items){
				frm.doc.items.forEach(function(row){
					frappe.model.set_value(row.doctype, row.name, 'billed_qty', null)
					frappe.model.set_value(row.doctype, row.name, 'physically_verified_quantity', null)
					frappe.model.set_value(row.doctype, row.name, 'received_qty', null)
					frappe.model.set_value(row.doctype, row.name, 'qty', null)
					frappe.model.set_value(row.doctype, row.name, 'rejected_qty', null)
					frappe.model.set_value(row.doctype, row.name, 'short_quantity', null)
					frappe.model.set_value(row.doctype, row.name, 'excess_quantity', null)
					frappe.model.set_value(row.doctype, row.name, 'actual_accepted_qty', null)
					frappe.model.set_value(row.doctype, row.name, 'custom_rejected_qty', null)
				});
			}
		}
	},
	refresh: function(frm){
		if(frm.doc.is_return == 1){
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'short_quantity', cur_frm.doc.name);
			df.hidden = 1
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'excess_quantity', cur_frm.doc.name);
			df.hidden = 1
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'custom_rejected_qty', cur_frm.doc.name);
			df.hidden = 1
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'actual_accepted_qty', cur_frm.doc.name);
			df.read_only = 1
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'received_stock_qty', cur_frm.doc.name);
			df.hidden = 1
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'stock_qty', cur_frm.doc.name);
			df.hidden = 1

		}
		if(frm.doc.workflow_state == 'Draft'){
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'quality_inspection', cur_frm.doc.name);
			df.hidden = 1
		}
		if(frm.doc.workflow_state == 'Pending For QC'){
			var df = frappe.meta.get_docfield('Purchase Receipt Item', 'quality_inspection', cur_frm.doc.name);
			df.hidden = 0
		}
		if(frm.doc.is_return == 1){
			frm.set_df_property('set_warehouse', 'reqd', 1)
			refresh_field('set_warehouse')
		}
	},
	set_warehouse: function(frm){
		if(frm.doc.is_return == 1){
			frm.set_df_property('set_warehouse', 'reqd', 1)
			refresh_field('set_warehouse')
		}
	}
});


frappe.ui.form.on("Purchase Receipt Item", {
	billed_qty :function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
		var diff = flt(row.physically_verified_quantity - row.billed_qty)

		if (diff < 0){
			frappe.model.set_value(cdt, cdn, 'short_quantity', Math.abs(diff));
			frappe.model.set_value(cdt, cdn, 'excess_quantity', 0);
			frm.refresh_field("short_quantity");
			frm.refresh_field("excess_quantity");
		}
		else if(diff >= 0){
			frappe.model.set_value(cdt, cdn, 'excess_quantity', Math.abs(diff));
			frappe.model.set_value(cdt, cdn, 'short_quantity', 0);
			frm.refresh_field("short_quantity");
			frm.refresh_field("excess_quantity");
		}
		// var received_qty =  row.billed_qty + row.custom_rejected_qty
		// frappe.model.set_value(cdt, cdn, 'received_qty', received_qty);
		// frm.refresh_field("received_qty");
		frappe.model.set_value(cdt, cdn, 'qty', row.billed_qty);
		frm.refresh_field("qty");
		var accepted_qty = row.billed_qty - row.short_quantity + row.excess_quantity - row.custom_rejected_qty
		frappe.model.set_value(cdt, cdn, 'actual_accepted_qty', accepted_qty);		
		frm.refresh_field("actual_accepted_qty");
	},
	physically_verified_quantity :function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
		var diff = flt(row.physically_verified_quantity - row.billed_qty)

		if (diff < 0){
			frappe.model.set_value(cdt, cdn, 'short_quantity', Math.abs(diff));
			frappe.model.set_value(cdt, cdn, 'excess_quantity', 0);
			frm.refresh_field("short_quantity");
			frm.refresh_field("excess_quantity");
		}
		else if(diff >= 0){
			frappe.model.set_value(cdt, cdn, 'excess_quantity', Math.abs(diff));
			frappe.model.set_value(cdt, cdn, 'short_quantity', 0);
			frm.refresh_field("short_quantity");
			frm.refresh_field("excess_quantity");
		}
		// var received_qty =  row.billed_qty + row.custom_rejected_qty
		// frappe.model.set_value(cdt, cdn, 'received_qty', received_qty);
		// frm.refresh_field("received_qty");
		frappe.model.set_value(cdt, cdn, 'qty', row.billed_qty);
		frm.refresh_field("qty");
		var accepted_qty = row.billed_qty - row.short_quantity + row.excess_quantity - row.custom_rejected_qty
		frappe.model.set_value(cdt, cdn, 'actual_accepted_qty', accepted_qty);		
		frm.refresh_field("actual_accepted_qty");
	},
	custom_rejected_qty:function(rm,cdt,cdn){
		var row = locals[cdt][cdn]
		var diff = flt(row.physically_verified_quantity - row.billed_qty)

		if (diff < 0){
			frappe.model.set_value(cdt, cdn, 'short_quantity', Math.abs(diff));
			frappe.model.set_value(cdt, cdn, 'excess_quantity', 0);
			frm.refresh_field("short_quantity");
			frm.refresh_field("excess_quantity");
		}
		else if(diff >= 0){
			frappe.model.set_value(cdt, cdn, 'excess_quantity', Math.abs(diff));
			frappe.model.set_value(cdt, cdn, 'short_quantity', 0);
			frm.refresh_field("short_quantity");
			frm.refresh_field("excess_quantity");
		}
		// var received_qty =  row.billed_qty + row.custom_rejected_qty
		// frappe.model.set_value(cdt, cdn, 'received_qty', received_qty);
		// frm.refresh_field("received_qty");
		frappe.model.set_value(cdt, cdn, 'qty', row.billed_qty);
		frm.refresh_field("qty");
		var accepted_qty = row.billed_qty - row.short_quantity + row.excess_quantity - row.custom_rejected_qty
		frappe.model.set_value(cdt, cdn, 'actual_accepted_qty', accepted_qty);		
		frm.refresh_field("actual_accepted_qty");
	},
	quality_inspection:function(frm,cdt,cdn) {
		var row = locals[cdt][cdn]
		
		if (row.quality_inspection){

			frappe.call({
				method:"frappe.client.get_list",
					args:{
						doctype:"Quality Inspection",
						filters: [	["name","=",row.quality_inspection ] ],
						fields: ["rejected_warehouse","rejected_quantity"]
					},
				callback: function(r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, 'rejected_warehouse', r.message[0]['rejected_warehouse']);
						frappe.model.set_value(cdt, cdn, 'custom_rejected_qty',r.message[0]['rejected_quantity']);
						frm.refresh_field("rejected_warehouse");
						frm.refresh_field("rejected_quantity");

						// to update accepted qty
						var row = locals[cdt][cdn]
						var diff = flt(row.physically_verified_quantity - row.billed_qty)

						if (diff < 0){
							frappe.model.set_value(cdt, cdn, 'short_quantity', Math.abs(diff));
							frappe.model.set_value(cdt, cdn, 'excess_quantity', 0);
							frm.refresh_field("short_quantity");
							frm.refresh_field("excess_quantity");
						}
						else if(diff >= 0){
							frappe.model.set_value(cdt, cdn, 'excess_quantity', Math.abs(diff));
							frappe.model.set_value(cdt, cdn, 'short_quantity', 0);
							frm.refresh_field("short_quantity");
							frm.refresh_field("excess_quantity");
						}
						// var received_qty =  row.billed_qty + row.custom_rejected_qty
						// frappe.model.set_value(cdt, cdn, 'received_qty', received_qty);
						// frm.refresh_field("received_qty");
						frappe.model.set_value(cdt, cdn, 'qty', row.billed_qty);
						frm.refresh_field("qty");
						var accepted_qty = row.billed_qty - row.short_quantity + row.excess_quantity - row.custom_rejected_qty
						frappe.model.set_value(cdt, cdn, 'actual_accepted_qty', accepted_qty);		
						frm.refresh_field("actual_accepted_qty");
						
					}
				}
			});		

		}
	}
	
});

