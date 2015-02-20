# Copyright (c) 2013, Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, _, throw

class ToolsAllocation(Document):
	def assign1(self):
		for d in self.get('tools_info'):
			if d.status=='Assign':
				serial_no_details=frappe.db.sql("select name from `tabAssigned Tools` where serial_no='%s'"%(d.serial_no),as_list=1)
				if not serial_no_details:
					at = frappe.new_doc('Assigned Tools')
					at.employee_name = d.employee_name
					at.employee_code = d.employee_code
					at.item_code = d.item_code
					at.item_name = d.item_name
					at.status=d.status
					at.serial_no=d.serial_no
					at.tool_request=d.tool_request
					at.save(ignore_permissions =True)
					sr = frappe.get_doc("Serial No", d.serial_no)
					sr.status = "Not Available"
					sr.save()
			elif d.status=='Return':
				frappe.db.sql("Update `tabAssigned Tools` set status='Return' where serial_no='%s'"%(d.serial_no))
				sr = frappe.get_doc("Serial No", d.serial_no)
				sr.status = "Available"
				sr.save()

	def check_availabilty(self,data):
		serial_no_details= frappe.db.sql("select name from `tabAssigned Tools` where serial_no='%s' and status='Assign'"%(data),as_list=1)
		if serial_no_details:
			msgprint("Serial No is already allocated")
		else:
			pass

	def get_details(self,data):
		if data=='Pending':
			self.set('tools_info', [])
			tool_details= frappe.db.sql("""select employee_name,employee_code,item_code,item_name,name from 
				`tabRequest Of Tools` where docstatus=1 and name not in(select tool_request from `tabAssigned Tools`) order by creation desc; """,as_list=1)
			if tool_details:
				for tool in tool_details:
					e = self.append('tools_info', {})
					e.employee_name = tool[0]
					e.employee_code = tool[1]
					e.item_code = tool[2]
					e.item_name = tool[3]
					e.tool_request=tool[4]
					e.status='Pending'
					# e.serial_no=tool[5]
		elif data=='Assign':
			self.set('tools_info', [])
			tool_details= frappe.db.sql("""select employee_name,employee_code,item_code,
				item_name,status,serial_no,tool_request from `tabAssigned Tools` where status='Assign'""",as_list=1)
			if tool_details:
				for tool in tool_details:
					e = self.append('tools_info', {})
					e.employee_name = tool[0]
					e.employee_code = tool[1]
					e.item_code = tool[2]
					e.item_name = tool[3]
					e.status=tool[4]
					e.serial_no=tool[5]
					e.tool_request=tool[6]
		else:
			self.set('tools_info', [])
			tool_details= frappe.db.sql("""select employee_name,employee_code,item_code,
				item_name,status,serial_no,tool_request from `tabAssigned Tools`""",as_list=1)
			if tool_details:
				for tool in tool_details:
					e = self.append('tools_info', {})
					e.employee_name = tool[0]
					e.employee_code = tool[1]
					e.item_code = tool[2]
					e.item_name = tool[3]
					e.status=tool[4]
					e.serial_no=tool[5]
					e.tool_request=tool[6]			
						
					
	


		
	    	
	




		











