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
		frappe.errprint("in the submit")
		self.update_stock_ledger()

	def update_stock_ledger(self):
		frappe.errprint("in the update")
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
		frappe.errprint(st.mtn_details[0].item_code)
		frappe.errprint(st.name)	
		frappe.errprint("Done")



			


	












	# def update_stock_ledger(self):
		# stock= {}
		# stock2={}	
		# self.set('entries', [])	
		# frappe.errprint("in the update_stock_ledger")
		# for d in self.get('tools_information'):
		# 	frappe.errprint(stock)
		# 	if d.purpose=='Allocate':
		# 		frappe.errprint("stock")
		# 		stock.append('all',[])
		# 		stock['purpose']="Material Issue"
		# 		stock['item_code'].append(d.item_code),
		# 		stock['item_name'].append(d.item_name),
		# 		stock['qty']=d.qty,
		# 		stock['uom']=d.stock_uom
		# 	else:
		# 		stock2['item_code']=d.item_code,
		# 		stock2['item_name']=d.item_name,
		# 		stock2['qty']=d.qty,
		# 		stock2['uom']=d.stock_uom
		#     	frappe.errprint(stock)
		# frappe.errprint(stock)
		# frappe.errprint(stock2)
		# self.make_entry(stock)
					
	def make_entry(self,stock):
		frappe.errprint(stock)
		# dic=eval(stock)
		frappe.errprint(stock["item_code"])
		st = frappe.new_doc("Stock Entry")
		st.purpose="Material Issue"
		st.set('mtn_details', [])
		e = st.append('mtn_details', {})
		# e.item_code=
		# st.save()
		# return st.name
		# e.update(stock)
		# frappe.errprint(self.get('mtn_details'))
		# for d in self.get('mtn_details'):
			# frappe.errprint(d.item_code)
			# frappe.errprint(e)

	# def make_child(self,stock,parent)
	# 	std = frappe.new_doc("Stock Entry Detail")
	# 	std.
		# st.purpose="Material Issue"



				



