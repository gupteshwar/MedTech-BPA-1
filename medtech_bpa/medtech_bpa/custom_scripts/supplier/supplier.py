from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import nowdate, nowtime, today
from frappe.utils import cstr, flt, cint, nowdate, add_days, comma_and, now_datetime, ceil
import json, copy
from frappe import msgprint, _
from six import string_types, iteritems

def validate(doc, method):
    if not doc.custom_supplier_code:
        # Fetch the largest numeric custom_supplier_code
        last_supplier_code = frappe.db.sql(
            """
            SELECT custom_supplier_code 
            FROM `tabSupplier` 
            WHERE custom_supplier_code REGEXP '^[0-9]+$'
            ORDER BY CAST(custom_supplier_code AS UNSIGNED) DESC 
            LIMIT 1
            """,
            as_dict=True
        )

        if last_supplier_code and last_supplier_code[0].get("custom_supplier_code"):
            new_code = str(cint(last_supplier_code[0]["custom_supplier_code"]) + 1)
        else:
            frappe.throw(_("No existing supplier codes found. Please set the first Supplier Code manually."))

        # Assign the new code as a string
        doc.custom_supplier_code = new_code