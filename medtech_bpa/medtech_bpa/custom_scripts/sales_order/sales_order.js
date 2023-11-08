frappe.ui.form.on("Sales Order", {
	refresh: function(frm){
		if(frm.doc.docstatus===0 && !in_list(["Lost", "Stopped", "Closed"], frm.doc.status)) {
			frm.page.add_menu_item(__('Send Email'), function() {
				frm.trigger('send_email');
			});
		}
		
		if (frm.doc.workflow_state=="Rejected"){
			frappe.db.get_value('Comment', {'reference_name': frm.doc.name, 'comment_type':"Comment"}, 'name', (r) => {
				if (!r.name){
					frm.trigger('reason_of_rejection')
				}
			});
			frm.add_custom_button(__('Reason of Rejection'), function () {
				frm.trigger('reason_of_rejection')
			})
		}

	},

	send_email: function(frm) {
		frappe.call({
			method: "medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.send_so_notification",
			args: {
				"sales_order": frm.doc.name
			},
			callback: function(r) {
				console.log(r.message)
				if(!r.exc) {
					frappe.msgprint(__("Sending Email ... {}", [r.message]))
				}
			}
		});
	},

	reason_of_rejection: function(frm) {
		const dialog = new frappe.ui.Dialog({
			title: __("Reason of Rejection"),
			fields: [
				{
	              	label: __(''),
	              	fieldname: "rejection_reason",
	              	fieldtype: "Small Text",
	              	read_only: 0,
	              	reqd: 1, 
	            }
	        ],
			primary_action: function() {
				var data = dialog.get_values();
				frappe.call({
					method: "medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.reason_of_rejection",
					args: {
						reason: data.rejection_reason,
						name: frm.doc.name					
					},
					callback: function(r) {
						frm.reload_doc();
					}
				});
				dialog.hide();
			},
			primary_action_label: __('Update')
		});
		dialog.show();
	},
	before_save(frm) {
        frm.doc.items.forEach(row=>{
            if (row.discount_percentage !=0 && row.spl_disc !=0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount != 1){
                console.log("!!! !!!!!!1")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.spl_disc_amt = row.dis_amt_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.dis_amt_rate - row.spl_disc_amt
                row.disc_amt = row.discount_amounts * row.qty
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.discount_percentage !=0 && row.spl_disc !=0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!!11")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.spl_disc_amt = row.dis_amt_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.dis_amt_rate - row.spl_disc_amt
                row.disc_amt = row.discount_amounts * row.qty
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            } 
            else if (row.discount_percentage !=0 && row.spl_disc == 0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount != 1){
                console.log("!!! !!!!!2")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.disc_amt = row.discount_amounts * row.qty
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate

            }
            else if (row.discount_percentage !=0 && row.spl_disc == 0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!22")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.disc_amt = row.discount_amounts * row.qty
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            } 
            else if (row.discount_percentage == 0 && row.spl_disc != 0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount != 1){
                console.log("!!! !!!!!3")
                row.spl_disc_amt = row.price_list_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.price_list_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.discount_percentage == 0 && row.spl_disc != 0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!33")
                row.spl_disc_amt = row.price_list_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.price_list_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.discount_percentage == 0 && row.spl_disc == 0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount != 1){
                console.log("@@@@@@@@@@@@@@@@")
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate   
            }
            else if (row.discount_percentage == 0 && row.spl_disc == 0 && row.free_qty == 0 && row.additional_spl_disc == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("@@@@@@@@@@@@@@@@1")
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate   
            }
           // calculation base on free qty 
           else if (row.discount_percentage != 0 && row.spl_disc != 0 && row.free_qty != 0 && row.fully_discount != 1){
                console.log("!!! !!!!!4")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.spl_disc_amt = row.dis_amt_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.dis_amt_rate - row.spl_disc_amt
                row.disc_amt = row.discount_amounts * row.qty
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.free_qty * row.spl_disc_amt_rate
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.discount_percentage != 0 && row.spl_disc != 0 && row.free_qty != 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!44")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.spl_disc_amt = row.dis_amt_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.dis_amt_rate - row.spl_disc_amt
                row.disc_amt = row.discount_amounts * row.qty
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.free_qty * row.spl_disc_amt_rate
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            } 
            else if (row.discount_percentage != 0 && row.spl_disc == 0 && row.free_qty !=  0 && row.fully_discount != 1){
                console.log("!!! !!!!!5")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.disc_amt = row.discount_amounts * row.qty
                row.additional_spl_disc_amt = row.free_qty * row.dis_amt_rate
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.additional_spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
    
            }
            else if (row.discount_percentage != 0 && row.spl_disc == 0 && row.free_qty !=  0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!55")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.disc_amt = row.discount_amounts * row.qty
                row.additional_spl_disc_amt = row.free_qty * row.dis_amt_rate
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                row.rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.additional_spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
    
            }
            else if (row.discount_percentage == 0 && row.spl_disc != 0 && row.free_qty != 0 && row.fully_discount != 1){
                console.log("!!! !!!!!6")
                row.spl_disc_amt = row.price_list_rate * (row.spl_disc / 100)
                console.log(row.spl_disc_amt)
                row.spl_disc_amt_rate = row.price_list_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.free_qty * row.spl_disc_amt_rate
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate =row.spl_disc_amt_rate -(row.additional_spl_disc_amt / row.qty)
                row.rate = row.additional_spl_disc_amt_rate
                row.base_rate = row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.additional_spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
                
    
            }
            else if (row.discount_percentage == 0 && row.spl_disc != 0 && row.free_qty != 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!66")
                row.spl_disc_amt = row.price_list_rate * (row.spl_disc / 100)
                console.log(row.spl_disc_amt)
                row.spl_disc_amt_rate = row.price_list_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.free_qty * row.spl_disc_amt_rate
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate =row.spl_disc_amt_rate -(row.additional_spl_disc_amt / row.qty)
                row.rate = row.additional_spl_disc_amt_rate
                row.base_rate = row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.additional_spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
                
    
            }
            else if (row.discount_percentage == 0 && row.spl_disc == 0 && row.free_qty != 0 && row.fully_discount != 1){
                console.log("!!! !!!!!6 direct free qty")
                row.additional_spl_disc_amt = row.free_qty * row.price_list_rate
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate =row.additional_spl_disc_amt / row.qty
                row.rate = row.price_list_rate -row.additional_spl_disc_amt_rate
                console.log(row.price_list_rate, row.additional_spl_disc_amt_rate)
                row.base_rate =row.price_list_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.additional_spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
                
    
            }
            else if (row.discount_percentage == 0 && row.spl_disc == 0 && row.free_qty != 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!6222222222 direct free qty")
                row.additional_spl_disc_amt = row.free_qty * row.price_list_rate
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate =row.additional_spl_disc_amt / row.qty
                row.rate = row.price_list_rate -row.additional_spl_disc_amt_rate
                console.log(row.price_list_rate, row.additional_spl_disc_amt_rate)
                row.base_rate =row.price_list_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.additional_spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
                
    
            }

            // calculation base on  percentage
            else if (row.additional_spl_disc != 0 && row.discount_percentage != 0 && row.spl_disc != 0 && row.free_qty == 0 && row.fully_discount != 1){
                console.log("!!! !!!!!7")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.spl_disc_amt = row.dis_amt_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.dis_amt_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.disc_amt = row.discount_amounts * row.qty
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.spl_disc_amt_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.additional_spl_disc != 0 && row.discount_percentage != 0 && row.spl_disc != 0 && row.free_qty == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!77")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.spl_disc_amt = row.dis_amt_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.dis_amt_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.disc_amt = row.discount_amounts * row.qty
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.spl_disc_amt_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.additional_spl_disc != 0 && row.discount_percentage != 0 && row.spl_disc == 0 && row.free_qty == 0 && row.fully_discount != 1){
                console.log("!!! !!!!!8")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.disc_amt = row.discount_amounts * row.qty
                row.additional_spl_disc_amt = row.dis_amt_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.additional_spl_disc != 0 && row.discount_percentage != 0 && row.spl_disc == 0 && row.free_qty == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!88")
                row.discount_amounts = row.price_list_rate * (row.discount_percentage / 100)
                row.dis_amt_rate = row.price_list_rate - row.discount_amounts
                row.disc_amt = row.discount_amounts * row.qty
                row.additional_spl_disc_amt = row.dis_amt_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.dis_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            } 
            else if (row.additional_spl_disc != 0 && row.discount_percentage == 0 && row.spl_disc != 0 && row.free_qty == 0 && row.fully_discount != 1){
                console.log("!!! !!!!!9")
                row.spl_disc_amt = row.price_list_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.price_list_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.spl_disc_amt_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.additional_spl_disc != 0 && row.discount_percentage == 0 && row.spl_disc != 0 && row.free_qty == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!99")
                row.spl_disc_amt = row.price_list_rate * (row.spl_disc / 100)
                row.spl_disc_amt_rate = row.price_list_rate - row.spl_disc_amt
                console.log(row.spl_disc_amt_rate)
                row.total_spl_disc_amt = row.spl_disc_amt * row.qty
                row.additional_spl_disc_amt = row.spl_disc_amt_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.spl_disc_amt_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.additional_spl_disc != 0 && row.discount_percentage == 0 && row.spl_disc == 0 && row.free_qty == 0 && row.fully_discount != 1){
                console.log("!!! !!!!!10")
                row.additional_spl_disc_amt = row.price_list_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            }
            else if (row.additional_spl_disc != 0 && row.discount_percentage == 0 && row.spl_disc == 0 && row.free_qty == 0 && row.fully_discount == 1 && frm.doc.docstatus == 0 && row.price_list_rate != 0){
                console.log("!!! !!!!!110")
                row.additional_spl_disc_amt = row.price_list_rate * (row.additional_spl_disc/100) * row.qty
                console.log(row.additional_spl_disc_amt)
                row.additional_spl_disc_amt_rate = row.additional_spl_disc_amt / row.qty
                console.log(row.additional_spl_disc_amt_rate)
                row.rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.base_rate = row.price_list_rate - row.additional_spl_disc_amt_rate
                row.total_dis_for_qty = row.qty * (row.discount_amounts + row.spl_disc_amt)
                row.price_list_rate = 0
                row.amount = row.qty * row.rate
                row.base_amount = row.qty * row.rate
                row.net_amount = row.qty * row.rate
                row.base_net_amount = row.qty * row.rate
            } 
        })
        frm.refresh_field("items")
    }
})