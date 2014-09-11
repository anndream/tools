# Copyright (c) 2013, Indictrans and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('Size')

class TestSize(unittest.TestCase):
	pass
