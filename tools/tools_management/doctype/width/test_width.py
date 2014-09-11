# Copyright (c) 2013, Indictrans and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('Width')

class TestWidth(unittest.TestCase):
	pass
