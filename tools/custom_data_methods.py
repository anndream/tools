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
import qrcode
import qrcode.image.pil
import qrcode.image.svg
import qrcode
import unidecode

def get_user_branch():
	return frappe.db.get_value('User', frappe.session.user, 'branch')

def get_branch_warehouse(branch):
	return frappe.db.get_value('Branch', branch, 'warehouse')

def get_branch_cost_center(branch):
	return frappe.db.get_value('Branch', branch, 'cost_center')


def gererate_QRcode(code, docname):
	site_name = get_site_name()
	path = os.path.abspath(os.path.join('.',site_name, 'public', 'files','QRCode'))
	directory = '/%s/%s/'%(path,docname)
		
	if not os.path.exists(directory):
		
		os.makedirs(directory)

	if directory:
		code1=code.replace("/","-")
		filpath = directory + code1
		qr = qrcode.QRCode(  version=1,
    		error_correction=qrcode.constants.ERROR_CORRECT_L,
    		box_size=4,
   		 	border=2);
		qr.add_data(code)
		qr.make(fit=True);		
		img= qr.make_image()
		image_file = open(filpath+".png",'w+')
		fulname=img.save(image_file)		
	return fulname or None	



			
def generate_barcode(code, docname):
	site_name = get_site_name()
	path = os.path.abspath(os.path.join('.',site_name, 'public', 'files','Barcode'))
	directory = '/%s/%s/'%(path,docname)
		

	if not os.path.exists(directory):		
		os.makedirs(directory)
		

	if directory:
		code1=code.replace("/","-")
		filpath = directory + code1

		barcode.PROVIDED_BARCODES
		EAN = barcode.get_barcode_class('Code39')	
		ean = EAN(code)
		ean.writer.set_options({"module_height":6.0})
		fullname = ean.save(filpath)
		return code1 or None


def update_serial_no(parent, serial_no, msg):
	frappe.db.sql("""update `tabProduction Status Detail`
		set msg='%s' where parent = '%s' and serial_no='%s'"""%(msg, parent, serial_no))

def find_next_process(parent, process_name, trials):
	cond = "1=1"
	if trials:
		cond = "trials = '%s'"%(trials)
	process = frappe.db.sql(""" select * from `tabProcess Log` 
						where idx > (select max(idx) from `tabProcess Log` where parent = '%s' and process_name = '%s' and %s) and parent = '%s' order by idx limit 1"""%(parent, process_name, cond, parent), as_dict=1)
	if process:
		for r in process:
			return r

def get_site_name():
	return frappe.local.site_path.split('/')[1]			