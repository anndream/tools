# Copyright (c) 2013, Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.stock.utils import update_bin
from frappe.utils import flt, cint
from frappe import msgprint, _
import frappe.defaults
from frappe.model.mapper import get_mapped_doc

class ToolsManager(Document):

	def allocate_tools1(self):
		# for d in doc.get('entries'):
		self.update_stock_ledger()

	def update_stock_ledger(self):
		st = frappe.new_doc("Stock Entry")
		st.purpose="Material Issue"
		st.set('mtn_details', [])
		for d in self.get('tools_information'):
			e = st.append('mtn_details', {})
			e.item_code=d.item_code,
			e.item_name=d.item_name,
			e.qty=d.qty,
			e.uom=d.stock_uom
		st.save(ignore_permissions=True)	
					
	def make_entry(self,stock):
		# dic=eval(stock)
		st = frappe.new_doc("Stock Entry")
		st.purpose="Material Issue"
		st.set('mtn_details', [])
		e = st.append('mtn_details', {})
		# e.item_code=
		# st.save()
		# return st.name
		# e.update(stock)
		# for d in self.get('mtn_details'):
			# frappe.errprint(d.item_code)
			# frappe.errprint(e)

	# def make_child(self,stock,parent)
	# 	std = frappe.new_doc("Stock Entry Detail")
	# 	std.
		# st.purpose="Material Issue"



				



