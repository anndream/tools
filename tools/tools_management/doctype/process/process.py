# Copyright (c) 2013, Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Process(Document):
	def on_update(self):
		if not frappe.db.get_value('Activity Type',self.process_name, 'name'):
			s = frappe.new_doc('Activity Type')
			s.activity_type = self.process_name
			s.save(ignore_permissions= True)