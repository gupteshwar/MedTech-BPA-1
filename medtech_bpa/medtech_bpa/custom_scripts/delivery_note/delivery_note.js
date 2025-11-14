frappe.ui.form.on('Delivery Note', {
    // refresh(frm,cdt, cdn) {
    //     frm.doc.items.forEach(i=>{

    //         if (i.fully_discount == 1 && i.against_sales_order != null && frm.doc.__islocal){
    //                 i.price_list_rate = i.fully_discount_rate;
    //             } 
    //         //! Setting the MRP
    //         //!================================================================
    //         if (i.against_sales_order != null){
    //            frappe.call({
    //             method: 'medtech_bpa.medtech_bpa.custom_scripts.delivery_note.delivery_note.get_mrp_against_sales_order',
    //             args:{
    //                 'sales_order':i.against_sales_order,
    //                 'item_code':i.item_code
    //             },
    //             callback: function(r) {
    //                 // if (r.message.length > 0){
    //                 //     i.custom_mrp = r.message[0].custom_mrp
                        
    //                 //     }
    // //                 if (r.message !== undefined && r.message !== null) {
    //                     i.custom_mrp = r.message;   // directly set numeric value
    //                 }
    //                  }
    //                 })
    //              } 
    //             //!================================================================
        
            
            
    //         }
            
        
    //     )

    //     frm.refresh_field("items")
    // },

    before_save(frm) {
        
        frm.doc.items.forEach(i=>{

            if (i.fully_discount == 1 && i.against_sales_order != null && frm.doc.__islocal){
                    i.price_list_rate = i.fully_discount_rate;
                } 
            //! Setting the MRP
            if (i.against_sales_order != null){
               frappe.call({
                method: 'medtech_bpa.medtech_bpa.custom_scripts.delivery_note.delivery_note.get_mrp_against_sales_order',
                args:{
                    'sales_order':i.against_sales_order,
                    'item_code':i.item_code
                },
                callback: function(r) {
                    if (r.message) {
                        i.custom_mrp = r.message;  
                        frm.refresh_field("items")
                    }
                     }
                    })
                 } 
                //!================================================================
            }
        )
        

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
    },
    
   onload: function(frm) {
    if (!frm.doc.items || frm.doc.items.length === 0) return;

    const sales_orders = frm.doc.items
        .filter(item => item.against_sales_order)
        .map(item => item.against_sales_order);

    if (sales_orders.length === 0) return;

    // Use the first available sales order
    const sales_order = sales_orders[0];
    frappe.db.get_doc('Sales Order', sales_order).then(so => {
        // Set fields from Sales Order
        frm.set_value('custom_consignee_name', so.customer_name);

        // Convert HTML address_display to plain text
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = so.address_display || '';
        const plainAddress = tempDiv.textContent || tempDiv.innerText || '';
        frm.set_value('custom_consignee_address_', plainAddress);

        // Fetch and set Address details
        if (so.shipping_address_name) {
            frappe.db.get_doc('Address', so.shipping_address_name).then(addr => {
                frm.set_value('custom_consignee_city', addr.city || '');
                frm.set_value('custom_consignee_country', addr.country || '');
                frm.set_value('custom_consignee_state', addr.state || addr.state_or_province || '');
                frm.set_value('custom_consignee_postal_code', addr.pincode || '');
                frm.set_value('custom_consignee_contact', addr.phone || '');

                frm.refresh_fields();
            });
        }
    });
}
        
})     
             


     




    