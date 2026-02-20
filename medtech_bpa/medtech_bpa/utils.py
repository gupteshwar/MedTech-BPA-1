import frappe
from frappe.utils import now_datetime, time_diff_in_hours,pretty_date, now, add_to_date
from datetime import datetime, date
from email.utils import formataddr
from frappe.utils import nowdate, getdate
def delete_email_queues():
    # '''method deletes email queues whose status is in Sent and/or Error'''
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! weekday ---", frappe.utils.get_datetime().weekday() )

    #checking the day of the week, the script only works on monday, wednesday and friday
    # if not frappe.utils.get_datetime().weekday() in [1,3,5,6]:
    c = str(now_datetime())[11:13]
    d = int(c)
    a = "01"
    b = int(a)
    if frappe.utils.get_datetime().weekday() in [0,1,2,3,4,5,6] and d == b:

        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        #getting the tuple of names of Email Queues with status in Sent or Error
        deletable_email_queues_tuple = frappe.db.sql('''
        SELECT
            name
        FROM
            `tabEmail Queue`
        WHERE
            status
        IN
            ('Sent', 'Error')
        ''')
            
            #deleting the email queues in safe update mode
        frappe.db.sql('''
        DELETE FROM
            `tabEmail Queue`
        WHERE
            name
        IN
            %(deletable_email_queues)s;
        ''', values={'deletable_email_queues':deletable_email_queues_tuple})

def daily_credit_check():

    today = getdate(nowdate())

    invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "docstatus": 1,
            "outstanding_amount": (">", 0)
        },
        fields=["name", "customer", "posting_date", "due_date", "outstanding_amount"]
    )

    customer_data = {}

    for inv in invoices:

        if not inv.due_date or today < getdate(inv.due_date):
            continue

        if inv.customer not in customer_data:
            customer_data[inv.customer] = []

        customer_data[inv.customer].append(inv)

    for customer_name, inv_list in customer_data.items():

        customer = frappe.get_doc("Customer", customer_name)

        if not customer.custom_reminder_emails:
            continue

        recipients = [
            e.strip()
            for e in customer.custom_reminder_emails.replace("\n", ",").split(",")
            if e.strip()
        ]

        table_rows = ""
        total_outstanding = 0

        for inv in inv_list:
            total_outstanding += inv.outstanding_amount or 0

            table_rows += f"""
                <tr>
                    <td>{inv.name}</td>
                    <td>{customer.customer_name}</td>
                    <td>{frappe.utils.formatdate(inv.posting_date)}</td>
                    <td style="text-align:right;">₹{inv.outstanding_amount:,.2f}</td>
                </tr>
            """

        message = f"""
        <p>Dear Team,</p>

        <p>Please find below the outstanding invoices that are more than 30 days old.</p>

        <h3>Outstanding Invoices (More Than 30 Days)</h3>

        <table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse;">
            <tr style="background-color:#f2f2f2;">
                <th>Invoice No</th>
                <th>Customer</th>
                <th>Invoice Date</th>
                <th>Outstanding Amount</th>
            </tr>
            {table_rows}
        </table>

        <br>
        <p><b>Total Outstanding Amount: ₹{total_outstanding:,.2f}</b></p>

        <p>
        Kindly arrange the payment at the earliest.<br>
        If already paid, please ignore this email.
        </p>

        <p>Thank you.</p>
        """

        frappe.sendmail(
            recipients=recipients,
            subject="Outstanding More Than 30 Days",
            message=message
        )

        frappe.db.set_value("Customer", customer_name, "disabled", 1)

    frappe.db.commit()