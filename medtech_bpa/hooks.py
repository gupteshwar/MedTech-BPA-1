# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "medtech_bpa"
app_title = "MedTech-BPA"
app_publisher = "Indictrans"
app_description = "Business Process Automation for MedTech"
app_icon = "octicon octicon-plus"
app_color = "Blue"
app_email = "contact@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/medtech_bpa/css/medtech_bpa.css"
# app_include_js = "/assets/medtech_bpa/js/medtech_bpa.js"

# include js, css files in header of web template
# web_include_css = "/assets/medtech_bpa/css/medtech_bpa.css"
# web_include_js = "/assets/medtech_bpa/js/medtech_bpa.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "medtech_bpa.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "medtech_bpa.install.before_install"
# after_install = "medtech_bpa.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "medtech_bpa.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Eventas
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

#scheduler_events = {
# 	"all": [
# 		"medtech_bpa.tasks.all"
# 	],
	# "daily": [
	# 	"medtech_bpa.medtech_bpa.utils.delete_email_queues"
	# ],
	# "hourly": [
	# 	"medtech_bpa.medtech_bpa.utils.delete_email_queues"
	# ],
	# 	"monthly": [
	# 		"medtech_bpa.tasks.monthly"
	# 	]
# 	"weekly": [
# 		"medtech_bpa.medtech_bpa.utils.delete_email_queues"
# 	],
# 	"cron": {
#         "0 16 * * *": [  # Trigger at 4:00 PM daily
#             "medtech_bpa.email_cron.outstanding_invoice.send_invoice_summary_email"
#         ]
#     }
# }
scheduler_events = {
	
	"weekly": [
		"medtech_bpa.medtech_bpa.utils.delete_email_queues"
	],
	"cron": {
        "30 1 * * *": [  # Trigger at 4:00 PM daily
            "medtech_bpa.email_cron.outstanding_invoice.send_invoice_summary_email"
        ]
    }
}
# Testing
# -------

# before_tests = "medtech_bpa.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "medtech_bpa.vent.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "medtech_bpa.task.get_dashboard_data"
# }

fixtures = ['Custom Field', 'Property Setter', 'Print Format', 'Role', 
	'Letter Head', 'Print Style', 'Print Settings',
 	'Workflow', 'Workflow State', 'Workflow Action Master',"Client Script","Translation"]

doctype_js = {
	"Purchase Receipt" : "medtech_bpa/custom_scripts/purchase_receipt/purchase_receipt.js",
	"Item":	"medtech_bpa/custom_scripts/item/item.js",
	"Quality Inspection": "medtech_bpa/custom_scripts/quality_inspection/quality_inspection.js",
	"Production Plan":"medtech_bpa/custom_scripts/production_plan/production_plan.js",
	"Stock Entry":"medtech_bpa/custom_scripts/stock_entry/stock_entry.js",
	"Purchase Order":"medtech_bpa/custom_scripts/purchase_order/purchase_order.js",
	"Sales Order":"medtech_bpa/custom_scripts/sales_order/sales_order.js",
	"Sales Invoice":"medtech_bpa/custom_scripts/sales_invoice/sales_invoice.js",
	"Payment Entry":"medtech_bpa/custom_scripts/payment_entry/payment_entry.js",
	"Delivery Note":"medtech_bpa/custom_scripts/delivery_note/delivery_note.js",
}


doc_events = {
	"Purchase Receipt":{
		"validate":"medtech_bpa.medtech_bpa.custom_scripts.purchase_receipt.purchase_receipt.validate",
		#"before_save":"medtech_bpa.medtech_bpa.custom_scripts.purchase_receipt.purchase_receipt.before_save",
		"before_submit":"medtech_bpa.medtech_bpa.custom_scripts.purchase_receipt.purchase_receipt.before_submit",
		"on_submit": "medtech_bpa.medtech_bpa.custom_scripts.purchase_receipt.purchase_receipt.on_submit"	
	},
	"Quality Inspection":{
		"validate":"medtech_bpa.medtech_bpa.custom_scripts.quality_inspection.quality_inspection.validate",
		"on_submit": "medtech_bpa.medtech_bpa.custom_scripts.quality_inspection.quality_inspection.on_submit"
	},
	"Production Plan":{
	"validate":"medtech_bpa.medtech_bpa.custom_scripts.production_plan.production_plan.validate",
	"on_submit":"medtech_bpa.medtech_bpa.custom_scripts.production_plan.production_plan.on_submit"
	},
	"Work Order":{
	"on_submit":"medtech_bpa.medtech_bpa.custom_scripts.work_order.work_order.on_submit"
	},
	"Stock Entry":{
		"validate" : "medtech_bpa.medtech_bpa.custom_scripts.stock_entry.stock_entry.after_insert",
		"on_submit" : "medtech_bpa.medtech_bpa.custom_scripts.stock_entry.stock_entry.on_submit"
	},
	"Purchase Invoice":{
		"validate":"medtech_bpa.medtech_bpa.custom_scripts.purchase_invoice.purchase_invoice.validate"
	},
	"BOM":{
	"autoname":"medtech_bpa.medtech_bpa.custom_scripts.bom.bom.autoname"
	},

	
	"Sales Order":{
		"on_update_after_submit":"medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.on_update_after_submit",
		"validate": ["medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.validate",
			"medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.update_rate_with_taxes"],
		"before_save":"medtech_bpa.medtech_bpa.custom_scripts.sales_order.sales_order.before_save",	
	},
	"Delivery Note":{
		"validate":"medtech_bpa.medtech_bpa.custom_scripts.delivery_note.delivery_note.validate",
		"before_save":"medtech_bpa.medtech_bpa.custom_scripts.delivery_note.delivery_note.before_save"
	},
	
	"Sales Invoice":{
		"validate":"medtech_bpa.medtech_bpa.custom_scripts.sales_invoice.sales_invoice.validate",
		"on_submit":"medtech_bpa.medtech_bpa.custom_scripts.sales_invoice.sales_invoice.on_submit",
		"before_save":"medtech_bpa.medtech_bpa.custom_scripts.sales_invoice.sales_invoice.before_save"

	}
}

import frappe
from frappe.utils import flt,today, get_link_to_form
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate
from erpnext.accounts.utils import get_account_currency, get_fiscal_year
from frappe import _
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
def validate_supplier_invoice_no(self):
		if self.bill_date:
			if getdate(self.bill_date) > getdate(self.posting_date):
				frappe.throw(_("Supplier Invoice Date cannot be greater than Posting Date"))

		if self.bill_no:
			if cint(frappe.db.get_single_value("Accounts Settings", "check_supplier_invoice_uniqueness")):
				fiscal_year = get_fiscal_year(self.posting_date, company=self.company, as_dict=True)

				if not self.is_rate_differences__credit_note :
					pi = frappe.db.sql('''select name from `tabPurchase Invoice`
						where
							bill_no = %(bill_no)s
							and supplier = %(supplier)s
							and name != %(name)s
							and docstatus < 2
							and is_rate_differences__credit_note != 1
						 	and posting_date between %(year_start_date)s and %(year_end_date)s''', {
								"bill_no": self.bill_no,
								"supplier": self.supplier,
								"name": self.name,
								"year_start_date": fiscal_year.year_start_date,
								"year_end_date": fiscal_year.year_end_date
						 	})

					if pi:
						pi = pi[0][0]
						frappe.throw(_("Supplier Invoice No exists in Purchase1 Invoice {0}").format(pi))
PurchaseInvoice.validate_supplier_invoice=validate_supplier_invoice_no

