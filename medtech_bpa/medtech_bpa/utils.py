import frappe

def delete_email_queues():
    '''method deletes email queues whose status is in Sent and/or Error'''
    #added tuesday (1) in the condition for testing purposes only! should remove once confirmed
    if not frappe.utils.get_datetime().weekday() in [0, 1, 2, 4]:
        return
    deletable_email_queues_tuple = tuple(frappe.db.get_list('Email Queue', {'status':['in',['Sent', 'Error']]}, pluck = 'name'))
    frappe.db.sql('''
    DELETE FROM
        `tabEmail Queue`
    WHERE
        name
    IN
        %(deletable_email_queues)s;
    ''', values={'deletable_email_queues':deletable_email_queues_tuple})