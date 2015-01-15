# Copyright (c) 2013, Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class MeasurementFormula(Document):
	def validate(self):
		self.check_source_target()
	def check_source_target(self):
		parameter = []
		for d in self.get('measurement_rules'):
			if d.parameter == d.target_parameter or d.target_parameter in parameter:
				frappe.throw(_("Duplicate parameter at row {0}").format(d.idx))
			parameter.append(d.target_parameter)
