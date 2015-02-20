# Copyright (c) 2013, Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RequestOfTools(Document):
	def on_update(self):
		rt = frappe.new_doc('Requested Tools')
		rt.employee_name = self.employee_name
		rt.employee_code = self.employee_code
		rt.item_code = self.item_code
		rt.item_name = self.item_name
		rt.parent ='Tools Allocation'
		rt.parentfield = 'tools_info'
		rt.parenttype = 'Tools Allocation'
		rt.status='Pending'
		rt.tool_request=self.name
		rt.save(ignore_permissions =True)

