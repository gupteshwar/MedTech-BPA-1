import frappe
from frappe.utils import nowdate, add_days, formatdate

@frappe.whitelist()
def send_invoice_summary_email():
    # Calculate the target date (30 days before today)
    target_date = add_days(nowdate(), -30)
    
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
    
    # Group invoices by customer
    grouped_invoices = {}
    for invoice in invoices:
        customer = invoice["customer"]
        if customer not in grouped_invoices:
            grouped_invoices[customer] = []
        grouped_invoices[customer].append(invoice)
    
    # Recipients for the email
    recipients = ["akash@medtechlife.com", "sales2@medtechlife.com", "accounts6@medtechlife.com","priyatosh.s@indictranstech.com","pradip.s@indictranstech.com"]
    
    # Send separate email for each customer
    for customer, invoices in grouped_invoices.items():
        # Prepare email content
        email_content = f"<h3>Outstanding Invoices for {customer} (More Than 30 Days)</h3>"
        email_content += "<table border='1' style='width:100%; border-collapse: collapse;'>"
        email_content += "<tr><th>Invoice No</th><th>Invoice Date</th><th>Outstanding Amount</th></tr>"
        for invoice in invoices:
            email_content += f"<tr><td>{invoice['name']}</td><td>{formatdate(invoice['posting_date'])}</td><td>{invoice['outstanding_amount']}</td></tr>"
        email_content += "</table><br>"
        
        # Email subject
        subject = f"Outstanding More Than 30 Days for Customer: {customer}"
        
        # Send email for this customer
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=email_content
        )

# Schedule the task
def daily_invoice_summary_scheduler():
    send_invoice_summary_email()

# Hook this function to a daily scheduler in hooks.py
# hooks.py
# scheduler_events = {
#     "daily": [
#         "medtech_bpa.email_cron.outstanding_invoice.send_invoice_summary_email"
#     ]
# }
