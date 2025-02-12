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
    if doc.custom_supplier_code:
        # Split the supplier code and extract the numeric part
        parts = doc.custom_supplier_code.split('-')
        if len(parts) > 1:
            try:
                doc.custom_supplier_code_numeric = cint(parts[-1])
            except ValueError:
                frappe.throw(_("Invalid numeric value in custom_supplier_code: {0}").format(doc.custom_supplier_code))
    else:
        # Fetch the last custom_supplier_code_numeric from the database
        last_supplier = frappe.db.get_value("Supplier", {}, "custom_supplier_code_numeric", order_by="custom_supplier_code_numeric desc")
        
        if last_supplier:
            new_code_numeric = cint(last_supplier) + 1
        else:
            # If no previous numeric code exists, prompt the user to set it manually
            frappe.throw(_("No existing supplier codes found. Please set First Supplier Code manually."))

        # Generate new custom_supplier_code
        if doc.supplier_name:
            first_letter = doc.supplier_name[0].upper()  # Take the first letter of supplier_name
            doc.custom_supplier_code = f"{first_letter}-{new_code_numeric}"
             # Assign the new numeric code
            doc.custom_supplier_code_numeric = new_code_numeric
        
       