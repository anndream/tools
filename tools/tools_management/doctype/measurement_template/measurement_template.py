# Copyright (c) 2013, Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MeasurementTemplate(Document):
	def get_details(self,parameter):
		for d in self.get('measurement_table'):
			if d.parameter == parameter:
				d.abbreviation = frappe.db.get_value('Measurement',parameter,'abbreviation')
				d.value = frappe.db.get_value('Measurement',parameter,'default_value')
				d.image_view = frappe.db.get_value('Measurement',parameter,'user_image_show')
		return "Done"
