from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import nowdate,nowtime, today
from frappe.utils import cstr, flt, cint, nowdate, add_days, comma_and, now_datetime, ceil
import frappe, json, copy
from frappe import msgprint, _
from six import string_types, iteritems

# from frappe.model.document import Document


def validate(doc, method):
    if not doc.custom_supplier_code_numeric:
        # Fetch the latest and largest custom_supplier_code_numeric from the database
        last_supplier_numeric = frappe.db.get_value(
            "Supplier", {}, "custom_supplier_code_numeric", order_by="custom_supplier_code_numeric desc"
        )
        
        if last_supplier_numeric:
            new_code_numeric = cint(last_supplier_numeric) + 1
        else:
            # If no previous numeric code exists, prompt the user to set it manually
            frappe.throw(_("No existing supplier codes found. Please set the first Supplier Code manually."))
        
        # Assign the new numeric code
        doc.custom_supplier_code_numeric = new_code_numeric