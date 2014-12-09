# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

# IMPORTANT: only import safe functions as this module will be included in jinja environment
import frappe
import operator
import re, urllib, datetime, math
import babel.dates
import barcode
import os

def get_user_branch():
	return frappe.db.get_value('User', frappe.session.user, 'branch')

def get_branch_warehouse(branch):
	return frappe.db.get_value('Branch', branch, 'warehouse')

def get_branch_cost_center(branch):
	return frappe.db.get_value('Branch', branch, 'cost_center')

def generate_barcode(code, docname):
	path = os.path.abspath(os.path.join('.','bench_smart', 'public', 'files'))
	directory = '%s/%s'%(path, docname)
	if not os.path.exists(directory):
		os.makedirs(directory)

	if directory:
		filpath = directory + '/' + code
		barcode.PROVIDED_BARCODES
		EAN = barcode.get_barcode_class('Code39')
		ean = EAN(code)
		fullname = ean.save(filpath)
	return fullname or None

def update_serial_no(parent, serial_no, msg):
	frappe.db.sql("""update `tabProduction Status Detail`
		set msg='%s' where parent = '%s' and serial_no='%s'"""%(msg, parent, serial_no))

def find_next_process(parent, process_name, trials):
	cond = "1=1"
	if trials:
		cond = "trials = '%s'"%(trials)
	process = frappe.db.sql(""" select * from `tabProcess Log` 
						where idx > (select max(idx) from `tabProcess Log` where parent = '%s' and process_name = '%s' and %s) and parent = '%s' limit 1"""%(parent, process_name, cond, parent), as_dict=1)
	if process:
		for r in process:
			return r