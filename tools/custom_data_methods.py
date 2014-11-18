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
