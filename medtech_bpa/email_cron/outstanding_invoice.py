import frappe
from frappe.utils import nowdate, add_days, formatdate


@frappe.whitelist(allow_guest=True)
def send_invoice_summary_email():
    # Calculate the target date (30 days before today)
    target_date = add_days(nowdate(), -30)
    print("Target Date:", target_date)
    
    # Fetch invoices using Frappe ORM
    invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "posting_date": target_date,
            "docstatus": 1,  # Only include submitted invoices
            "outstanding_amount": [">", 0]  # Only include invoices with outstanding amount > 0
        },
        fields=["name", "customer", "outstanding_amount", "posting_date"]
    )
    
    print("Invoices:", invoices)
    
    
    # Recipients for the email
    recipients = [
        "akash@medtechlife.com", 
        "sales2@medtechlife.com", 
        "accounts6@medtechlife.com",
        "priyatosh.s@indictranstech.com", 
        "pradip.s@indictranstech.com",
        "priyatoshs.indictrans@gmail.com"
    ]
    
    # Fetch the sender email dynamically from the "Noreply" Email Account
    sender_email = frappe.db.get_value("Email Account", {"name": "Noreply"}, "email_id")
    if sender_email and len(invoices)>0:
            email_content = f"""
                <p>Dear Team,</p>
                <p>Please find below the outstanding invoices for that are more than 30 days old:</p>
                <h3>Outstanding Invoices for (More Than 30 Days)</h3>
                <table border='1' style='width:100%; border-collapse: collapse;'>
                    <tr>
                        <th>Invoice No</th>
                        <th>Customer</th>
                        <th>Invoice Date</th>
                        <th>Outstanding Amount</th>
                    </tr>
            """
            for invoice in invoices:
                email_content += f"""
                    <tr>
                        <td>{invoice['name']}</td>
                        <td>{invoice['customer']}</td>
                        <td>{formatdate(invoice['posting_date'])}</td>
                        <td>{invoice['outstanding_amount']}</td>
                    </tr>
                """
                
            email_content += """
                </table>
                <br>
                <p>We kindly request you to review and take the necessary action to clear these invoices at the earliest.</p>
                <p>Thank you for your prompt attention to this matter.</p>
                <p>Best regards,</p>
                <p>Medtech Life Pvt. Ltd.</p>
            """
                
                # Email subject
            subject = f"Outstanding More Than 30 Days"
            # Send email for this customer
            try:
                frappe.sendmail(
                    sender=sender_email,
                    recipients=recipients,
                    subject=subject,
                    message=email_content,
                    now=True
                )
                print(f"Email sent successfully")
                return {"invoices": invoices, "recipients": recipients, "sender_email": sender_email}
            except Exception as e:
                print(f"Error sending email for customer {e}")
                frappe.log_error(f"Error sending email for customer  {e}", "send_invoice_summary_email")
                return {"error": str(e)}
    
    else:
        return {"msg":"email not triggered",
                "sender_email": sender_email, 
                "invoices": invoices}      

    
