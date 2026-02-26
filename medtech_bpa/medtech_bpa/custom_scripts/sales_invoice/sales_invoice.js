frappe.ui.form.on('Sales Invoice', {
     validate: function(frm) {
        update_cc_emails(frm);   // save ke time force update
    },
    customer: function(frm) {
        update_cc_emails(frm);
        console.log("Customer Triggered");
        console.log("Selected Customer:", frm.doc.customer);

        if (!frm.doc.customer) {
            console.log("No customer selected");
            frm.set_value("custom_customer_email_id", "");
            return;
        }

        frappe.db.get_value('Customer', frm.doc.customer, 'email_id')
            .then(r => {

                console.log("Response from Customer:", r);

                if (r.message && r.message.email_id) {
                    console.log("Email Found:", r.message.email_id);
                    frm.set_value('custom_customer_email_id', r.message.email_id);
                } else {
                    console.log("Email NOT found in Customer");
                    frm.set_value('custom_customer_email_id', '');
                }

            }).catch(err => {
                console.log("Error while fetching email:", err);
            });
            // Update CC emails only if draft
            if (frm.doc.docstatus === 0) {
                update_cc_emails(frm);
            }
    },
    before_save: function(frm) {
        // Only update CC emails for draft
        if (frm.doc.docstatus === 0) {
            update_cc_emails(frm);
        }
    },
    refresh(frm) {
        // update_cc_emails(frm);
        frm.doc.items.forEach(i=>{
            if (i.fully_discount == 1 && i.sales_order != null && frm.doc.__islocal){
                i.price_list_rate = i.fully_discount_rate;
            }
            else if (i.fully_discount == 1 && i.delivery_note != null && frm.doc.__islocal){
                i.price_list_rate = i.fully_discount_rate;
            } 
            console.log("Sales Order: " + i.sales_order)
            //!setting up mrp
            if (i.delivery_note != null){
                frappe.call({
                    method: 'medtech_bpa.medtech_bpa.custom_scripts.delivery_note.delivery_note.custom_mrp_against_delivery_note',
                    args:{
                        'delivery_note':i.delivery_note,
                        'item_code':i.item_code
                    },
                    callback: function(r) {
                        if (r.message.length > 0){
                            i.custom_mrp = r.message[0].custom_mrp
                            }
                         }
                    })
                } 
            
            if (i.sales_order != null && frm.doc.__islocal){
                frappe.call({
                    method: 'medtech_bpa.medtech_bpa.custom_scripts.delivery_note.delivery_note.get_mrp_against_sales_order',
                    args:{
                        'sales_order':i.sales_order,
                        'item_code':i.item_code
                    },
                    callback: function(r) {
                        if (r.message.length > 0){
                            i.custom_mrp = r.message[0].custom_mrp
                            }
                        }
                        })
            }
            




        }) 
        frm.refresh_field("items")
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
    
});
// Trigger whenever a Sales Person is changed or added/removed
function update_cc_emails(frm) {

    if (!frm.doc.sales_team || frm.doc.sales_team.length === 0) {
        frm.set_value("custom_cc_email_ids", "");
        return;
    }

    let email_list = [];
    let promises = [];

    frm.doc.sales_team.forEach(row => {
        if (row.sales_person) {
            let p = frappe.db.get_value(
                "Sales Person",
                row.sales_person,
                "contact_company_email"
            ).then(r => {
                if (r.message && r.message.contact_company_email) {
                    email_list.push(r.message.contact_company_email.trim());
                }
            });

            promises.push(p);
        }
    });

    Promise.all(promises).then(() => {

        email_list = [...new Set(email_list)];
        let new_value = email_list.join(", ");
        let current_value = (frm.doc.custom_cc_email_ids || "").trim();

        if (current_value !== new_value) {
            frm.set_value("custom_cc_email_ids", new_value);
        }
    });
}