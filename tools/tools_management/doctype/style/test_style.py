# Copyright (c) 2013, Indictrans and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('Style')

class TestStyle(unittest.TestCase):
	pass
