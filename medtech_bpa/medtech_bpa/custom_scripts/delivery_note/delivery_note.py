from __future__ import unicode_literals
import frappe
from frappe import _



def validate(doc, method):
	so_name = [row.against_sales_order for row in doc.items if row.against_sales_order]
	if so_name:
		so_doc =frappe.get_doc("Sales Order", so_name[0])
		so_doc.workflow_state = "Pending Dispatch"
		so_doc.db_update()
		frappe.db.commit()


def before_save(doc,method):
	for row in doc.items:
		if row.fully_discount == 1 and row.fully_discount_rate == 0:
			frappe.throw(frappe._("Fully discount rate field is mandatory at row {0}.").format(row.idx))

