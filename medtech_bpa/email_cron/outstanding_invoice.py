import frappe
from frappe.utils import nowdate, add_days, formatdate


@frappe.whitelist(allow_guest=True)
def send_invoice_summary_email():
    # Calculate the target date (30 days before today)
    target_date = add_days(nowdate(), -30)
    print("Target Date:", target_date)

    # Fetch invoices using Frappe ORM
    invoices = frappe.db.get_list(
        "Sales Invoice",
        filters={
            "posting_date": target_date,
            "docstatus": 1,  # Only include submitted invoices
            "outstanding_amount": (">", 0)  # Only include invoices with outstanding amount > 0
        },
        fields=["name", "customer", "outstanding_amount", "posting_date"]
    )

    print("Invoices:", invoices)

    # Fetch recipient emails from Outstanding Invoice Email Settings
    email_settings = frappe.get_single("Outstanding Invoice Email Settings")
    
    if not email_settings:
        return {"error": "Outstanding Invoice Email Settings doctype not found"}

    recipients = [row.recipient_email for row in email_settings.get("recipient", []) if row.recipient_email]

    # Ensure the email is only triggered if the recipient list is not empty
    if not recipients:
        print("No recipients found, email not triggered.")
        return {"msg": "No recipients found, email not sent"}

    print("Recipients:", recipients)

    # Fetch the sender email dynamically from the "Noreply" Email Account
    sender_email = frappe.db.get_value("Email Account", {"name": "Noreply"}, "email_id")

    if sender_email and invoices:
        email_content = f"""
            <p>Dear Team,</p>
            <p>Please find below the outstanding invoices that are more than 30 days old:</p>
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
        subject = "Outstanding More Than 30 Days"

        # Send email
        try:
            email_summary_log=frappe.db.get_list("Invoice Summary Email Log",filters={
                "email_log_date":nowdate()
            })
            if len(email_summary_log)==0:
                
                frappe.sendmail(
                    sender=sender_email,
                    recipients=recipients,
                    subject=subject,
                    message=email_content,
                )
                print("Email sent successfully")
                # Log the email summary
                email_summary = frappe.new_doc("Invoice Summary Email Log")
                email_summary.email_log_date = nowdate()
                email_summary.save(ignore_permissions=True)
                return {"invoices": invoices, "recipients": recipients, "sender_email": sender_email}
            else:
                print("Email already sent for today")
                return {"msg": "Email already sent for today", "sender_email": sender_email, "invoices": invoices, "recipients": recipients}
        except Exception as e:
            print(f"Error sending email: {e}")
            frappe.log_error(f"Error sending email: {e}", "send_invoice_summary_email")
            return {"error": str(e)}

    else:
        return {"msg": "Email not triggered", "sender_email": sender_email, "invoices": invoices, "recipients": recipients}
