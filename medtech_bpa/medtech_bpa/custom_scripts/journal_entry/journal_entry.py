from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import nowdate,nowtime, today
import frappe, json, copy
from frappe import msgprint, _
from six import string_types, iteritems


def validate(doc,method):
	if doc.party_name is not None:
         supplier_code=frappe.db.get_value("Supplier",doc.party_name,"custom_supplier_code")
         if supplier_code:
              doc.custom_supplier_code=supplier_code
