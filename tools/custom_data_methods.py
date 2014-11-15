# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

# IMPORTANT: only import safe functions as this module will be included in jinja environment
import frappe
import operator
import re, urllib, datetime, math
import babel.dates

def get_user_branch():
	return frappe.db.get_value('User', frappe.session.user, 'branch')

def get_branch_warehouse(branch):
	return frappe.db.get_value('Branch', branch, 'warehouse')

def get_branch_cost_center(branch):
	return frappe.db.get_value('Branch', branch, 'cost_center')
