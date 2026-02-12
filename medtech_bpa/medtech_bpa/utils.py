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
        fields=["name", "customer", "due_date"]
    )

    customer_overdue = {}

    for inv in invoices:

        customer = frappe.get_doc("Customer", inv.customer)

        if not customer.custom_reminder_emails:
            continue

        recipients = [
            e.strip()
            for e in customer.custom_reminder_emails.replace("\n", ",").split(",")
            if e.strip()
        ]

        # send reminder from due date
        if today >= getdate(inv.due_date):
            frappe.sendmail(
                recipients=recipients,
                subject="Payment Reminder",
                message=f"Invoice {inv.name} payment pending. Kindly clear dues."
            )

        # mark overdue
        if today > getdate(inv.due_date):
            customer_overdue[customer.name] = 1

    # disable customers having overdue invoices
    for cust in customer_overdue:
        frappe.db.set_value("Customer", cust, "disabled", 1)

    frappe.db.commit()        
            