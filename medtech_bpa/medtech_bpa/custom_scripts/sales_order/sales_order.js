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
        
        // setTimeout(() => {
        //     frm.remove_custom_button('Reserve', 'Stock Reservation');
        // }, 10);
        
        // Add custom button and override the stock reservation function
        // frm.add_custom_button(__("Reserve"), function () {
        //     create_stock_reservation_entries_with_raw_materials(frm);
        // },__("Stock Reseration"));
        
        frm.add_custom_button(__('Material Request For RM'), function () {
            create_Material_request_raw_materials(frm);
        })
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

function create_stock_reservation_entries_with_raw_materials(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __("Stock Reservation"),
        size: "extra-large",
        fields: [
            {
                fieldname: "set_warehouse",
                fieldtype: "Link",
                label: __("Set Warehouse"),
                options: "Warehouse",
                default: frm.doc.set_warehouse,
                get_query: () => {
                    return {
                        filters: [["Warehouse", "is_group", "!=", 1]],
                    };
                },
                onchange: () => {
                    if (dialog.get_value("set_warehouse")) {
                        dialog.fields_dict.items.df.data.forEach((row) => {
                            if (row.is_raw_material == 0){
                                row.warehouse = dialog.get_value("set_warehouse");
                            }
                        });
                        dialog.fields_dict.items.grid.refresh();
                    }
                },
            },
            { fieldtype: "Column Break" },
            {
                fieldname: "add_item",
                fieldtype: "Link",
                label: __("Add Item"),
                options: "Sales Order Item",
                get_query: () => {
                    return {
                        query: "erpnext.controllers.queries.get_filtered_child_rows",
                        filters: {
                            parenttype: frm.doc.doctype,
                            parent: frm.doc.name,
                            reserve_stock: 1,
                        },
                    };
                },
                onchange: () => {
                    let sales_order_item = dialog.get_value("add_item");

                    if (sales_order_item) {
                        frm.doc.items.forEach((item) => {
                            if (item.name === sales_order_item) {
                                let unreserved_qty =
                                    (flt(item.stock_qty) -
                                        (item.stock_reserved_qty
                                            ? flt(item.stock_reserved_qty)
                                            : flt(item.delivered_qty) * flt(item.conversion_factor))) /
                                    flt(item.conversion_factor);

                                if (unreserved_qty > 0) {
                                    dialog.fields_dict.items.df.data.forEach((row) => {
                                        if (row.sales_order_item === sales_order_item) {
                                            unreserved_qty -= row.qty_to_reserve;
                                        }
                                    });
                                }

                                dialog.fields_dict.items.df.data.push({
                                    sales_order_item: item.name,
                                    item_code: item.item_code,
                                    warehouse: dialog.get_value("set_warehouse") || item.warehouse,
                                    qty_to_reserve: Math.max(unreserved_qty, 0),
                                    uom: item.uom, // Add UOM here
                                    rate: item.rate, // Add rate here
                                    amount: item.amount, // Add amount here
                                });
                                dialog.fields_dict.items.grid.refresh();
                                dialog.set_value("add_item", undefined);
                            }
                        });
                    }
                },
            },
            {
                fieldname: "raw_material_warehouse",
                fieldtype: "Link",
                label: __("Raw Material Warehouse"),
                options: "Warehouse",
                onchange: () => {
                    if (dialog.get_value("raw_material_warehouse")) {
                        dialog.fields_dict.items.df.data.forEach((row) => {
                            if (row.is_raw_material == 1){
                                row.warehouse = dialog.get_value("raw_material_warehouse");
                            }
                        });
                        dialog.fields_dict.items.grid.refresh();
                    }
                },
            },
            {
                fieldname: "get_raw_materials",
                fieldtype: "Check",
                label: __("Get Raw Materials"),
                onchange: () => {
                    let is_checked = dialog.get_value("get_raw_materials");
                    let grid = dialog.fields_dict.items.grid;
                    let old_items = [...grid.df.data]; // Create a shallow copy to avoid reference issues
                    // Add this flag to track if we've already shown the message
                    if (!dialog.raw_materials_fetched) {
                        dialog.raw_materials_fetched = false;
                    }
                    if (is_checked == 1) {
                        grid.df.data = []; // Clear the grid
                        frappe.call({
                            method: "medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.get_bom_materials_for_sales_order_item",
                            args: {
                                sales_order: frm.doc.name,
                            },
                            callback: function (r) {
                                if (r.message && r.message.length) {
                                    // Add old items back to grid
                                    old_items.forEach(mat => {
                                        grid.df.data.push({
                                            __checked: 1,
                                            sales_order_item: mat.sales_order_item,
                                            item_code: mat.item_code,
                                            warehouse: mat.warehouse,
                                            qty_to_reserve: mat.qty_to_reserve,
                                            uom: mat.uom, // Ensure UOM is added
                                            rate: mat.rate, // Ensure rate is added
                                            amount: mat.amount, // Ensure amount is added
                                            is_raw_material: mat.is_raw_material || 0, // Keep old state if exists
                                        });
                                    });

                                    // Add raw materials fetched from BOM
                                    r.message.forEach(mat => {
                                        let materialExists = grid.df.data.some(item => item.item_code === mat.item_code);
                                        if (!materialExists) {
                                            // Determine the warehouse for raw materials
                                            let warehouse = mat.is_raw_material ? dialog.get_value("raw_material_warehouse") || frm.doc.set_warehouse : frm.doc.set_warehouse;

                                            grid.df.data.push({
                                                item_code: mat.item_code,
                                                qty_to_reserve: mat.qty,
                                                uom: mat.uom, 
                                                rate: mat.rate, 
                                                amount: mat.amount,
                                                is_raw_material: 1,  // Mark as raw material
                                                warehouse: warehouse,  // Set the appropriate warehouse
                                                sales_order_item: mat.sales_order_item,
                                            });
                                        }
                                    });

                                    dialog.fields_dict.items.grid.refresh();

                                    // Only show msgprint once when raw materials are fetched FOR THE FIRST TIME
                                    if (r.message.length > 0 && !dialog.raw_materials_fetched) {
                                        frappe.msgprint("Raw materials fetched from BOMs.");
                                        dialog.raw_materials_fetched = true;
                                    }
                                } else {
                                    // No raw materials, show message only once
                                    if (!grid.df.data.length && !dialog.raw_materials_fetched) {
                                        frappe.msgprint("No BOMs found for items in this Sales Order.");
                                        dialog.raw_materials_fetched = true;
                                    }
                                }
                            }
                        });
                    } else if (is_checked != 1) {
                        // Filter out raw material items from the grid when checkbox is unchecked
                        grid.df.data = grid.df.data.filter(mat => mat.is_raw_material !== 1); // Remove rows with is_raw_material === 1
                        dialog.fields_dict.items.grid.refresh();
                    }
                }
            },
            { fieldtype: "Section Break" },
            {
                fieldname: "items",
                fieldtype: "Table",
                label: __("Items to Reserve"),
                allow_bulk_edit: false,
                cannot_add_rows: true,
                cannot_delete_rows: true,
                data: [],
                fields: [
                    {
                        fieldname: "sales_order_item",
                        fieldtype: "Link",
                        label: __("Sales Order Item"),
                        options: "Sales Order Item",
                        reqd: 1,
                        in_list_view: 1,
                        get_query: () => {
                            return {
                                query: "erpnext.controllers.queries.get_filtered_child_rows",
                                filters: {
                                    parenttype: frm.doc.doctype,
                                    parent: frm.doc.name,
                                    reserve_stock: 1,
                                },
                            };
                        },
                        onchange: (event) => {
                            if (event) {
                                let name = $(event.currentTarget).closest(".grid-row").attr("data-name");
                                let item_row = dialog.fields_dict.items.grid.grid_rows_by_docname[name].doc;

                                frm.doc.items.forEach((item) => {
                                    if (item.name === item_row.sales_order_item) {
                                        item_row.item_code = item.item_code;
                                    }
                                });
                                dialog.fields_dict.items.grid.refresh();
                            }
                        },
                    },
                    {
                        fieldname: "item_code",
                        fieldtype: "Link",
                        label: __("Item Code"),
                        options: "Item",
                        reqd: 1,
                        read_only: 1,
                        in_list_view: 1,
                    },
                    {
                        fieldname: "warehouse",
                        fieldtype: "Link",
                        label: __("Warehouse"),
                        options: "Warehouse",
                        reqd: 1,
                        in_list_view: 1,
                        get_query: () => {
                            return {
                                filters: [["Warehouse", "is_group", "!=", 1]],
                            };
                        },
                    },
                    {
                        fieldname: "qty_to_reserve",
                        fieldtype: "Float",
                        label: __("Qty"),
                        reqd: 1,
                        in_list_view: 1,
                    },
                    {
                        fieldname: "uom",
                        fieldtype: "Data",
                        label: __("UOM"),
                        reqd: 0,
                        in_list_view: 1,
                    },
                    {
                        fieldname: "rate",
                        fieldtype: "Currency",
                        label: __("Rate(INR)"),
                        reqd: 0,
                        in_list_view: 1,
                    },
                    {
                        fieldname: "amount",
                        fieldtype: "Currency",
                        label: __("Amount(INR)"),
                        reqd: 0,
                        in_list_view: 1,
                    },
                    {
                        fieldname: "is_raw_material",
                        fieldtype: "Check",
                        label: __("Is Raw Material"),
                        reqd: 0,
                        in_list_view: 1,
                    },
                ],
            },
        ],
        primary_action_label: __("Reserve Stock"),
        primary_action: () => {
            var data = { items: dialog.fields_dict.items.grid.get_selected_children() };

            if (data.items && data.items.length > 0) {
                frappe.call({
                    doc: frm.doc,
                    method: "create_stock_reservation_entries",
                    args: {
                        items_details: data.items,
                        notify: true,
                    },
                    freeze: true,
                    freeze_message: __("Reserving Stock..."),
                    callback: (r) => {
                        frm.doc.__onload.has_unreserved_stock = false;
                        frm.reload_doc();
                    },
                });
                dialog.hide();
            } else {
                frappe.msgprint(__("Please select items to reserve."));
            }
        },
    });

    // Initialize the raw_materials_fetched flag
    dialog.raw_materials_fetched = false;

    frm.doc.items.forEach((item) => {
        if (item.reserve_stock) {
            let unreserved_qty =
                (flt(item.stock_qty) -
                    (item.stock_reserved_qty
                        ? flt(item.stock_reserved_qty)
                        : flt(item.delivered_qty) * flt(item.conversion_factor))) /
                flt(item.conversion_factor);

            if (unreserved_qty > 0) {
                dialog.fields_dict.items.df.data.push({
                    __checked: 1,
                    sales_order_item: item.name,
                    item_code: item.item_code,
                    warehouse: item.warehouse,
                    qty_to_reserve: unreserved_qty,
                    uom: item.uom, // Ensure UOM is added
                    rate: item.rate, // Ensure rate is added
                    amount: item.amount, // Ensure amount is added
                });
            }
        }
    });

    dialog.fields_dict.items.grid.refresh();
    dialog.show();
}

function create_Material_request_raw_materials(frm) {
    frappe.call({
        method:"medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.create_material_request_from_bom",
        args:{
            sales_order:frm.doc.name
        },
        callback: function (r) {
            if (!r.exc && r.message) {
                frappe.set_route("Form", "Material Request", r.message);

            }
        }
    })
}

