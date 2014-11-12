# Copyright (c) 2013, Indictrans and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, _, throw

from frappe.utils import cstr, cint, flt, comma_or, nowdate


class ToolMaintenance(Document):
	def check_availabilty(self,data):
		serial_no_details= frappe.db.sql("select name from `tabAssigned Tools` where serial_no='%s'"%(data),as_list=1)
		if serial_no_details:
			msgprint("Serial No is already allocated")
		else:
			pass

	def get_maintenance_details(self):
		self.make_mat_issue()
		self.make_mat_receipt()	
		# self.render_table_data()
		return "Done"

	def render_table_data(self):
		item_details = frappe.db.sql("select * from `tabTool Allocation Items` where parenttype = 'Tool Maintenance' and status='out'", as_dict=1)
		self.set('tool_maintainance',[])
		if item_details:
			for d in item_details:
				tm = self.append('tool_maintainance',{})
				tm.item_code = d.item_code
				tm.item_name = d.item_name
				tm.status = d.status
				tm.serial_no = d.serial_no
				tm.serial_nos = d.serial_nos
		return "Done"

	def make_mat_issue(self):
		fin_dict=self.make_dict()
		st =frappe.new_doc("Stock Entry")
		st.set('mtn_details', [])
		st.purpose_type="Material Issue"
		self.update_stock(st,fin_dict['Out'])
		st.docstatus=0
		st.save(ignore_permissions=True)
		return "Done"

	def update_stock(self,st,fin_dict):
		for d in fin_dict:
			se= st.append('mtn_details', {})
			se.item_code=cstr(d['item_code'])
			se.item_name=cstr(d['item_name'])
			se.s_warehouse='Stores - I'
			se.expense_account='Stock Adjustment - I'
			se.buying_cost_center='Main - I'
			se.conversion_factor=flt(1)
			se.qty=flt(1)
			se.uom='Nos'
			se.serial_no=cstr(d['serial_no'])

	def make_mat_receipt(self):
		frappe.errprint("in the material Receipt")
		fin_dict=self.make_dict()
		frappe.errprint(fin_dict)
		ste =frappe.new_doc("Stock Entry")
		ste.set('mtn_details', [])
		ste.purpose_type= "Material Receipt"
		ste.purpose = 'Material Receipt'
		self.update_stock_for_receipt(ste,fin_dict['In'])
		ste.docstatus=0
		ste.save(ignore_permissions=True)
		return "Done"		

	def update_stock_for_receipt(self,ste,fin_dict):
		for d in fin_dict:
			e = ste.append('mtn_details', {})
			e.item_code=cstr(d['item_code'])
			e.item_name=cstr(d['item_name'])
			e.t_warehouse='Stores - I'
			e.expense_account='Stock Adjustment - I'
			e.buying_cost_center='Main - I'
			e.incoming_rate=flt(1)
			e.conversion_factor=flt(1)
			e.qty=flt(1)
			e.uom='Nos'
			e.serial_no=cstr(d['serial_no'])		


	def make_dict(self):
		st =frappe.new_doc("Stock Entry")	
		dict1={}
		dict1['Out']=[]
		dict1['In']=[]
		for d in self.get('tool_maintainance'):
			if d.status=="Out":
				subdict={}
				subdict['item_code']=cstr(d.item_code)
				subdict['item_name']=cstr(d.item_name)
				subdict['s_warehouse']='Stores - I'
				subdict['expense_account']='Stock Adjustment - I'
				subdict['buying_cost_center']='Main - I'
				subdict['conversion_factor']=flt(1)
				subdict['qty']=flt(1)
				subdict['uom']='Nos'
				subdict['buying_cost_center']='Nos'
				subdict['serial_no']=cstr(d.serial_no)
				dict1['Out'].append(subdict)
			else:
				subdict={}
				subdict['item_code']=cstr(d.item_code)
				subdict['item_name']=cstr(d.item_name)
				subdict['t_warehouse']='Stores - I'
				subdict['expense_account']='Stock Adjustment - I'
				subdict['buying_cost_center']='Main - I'
				subdict['conversion_factor']=flt(1)
				subdict['qty']=flt(1)
				subdict['uom']='Nos'
				subdict['buying_cost_center']='Nos'
				subdict['serial_no']=cstr(d.serial_no)
				dict1['In'].append(subdict)
		return dict1
	
