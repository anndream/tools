from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"label": _("Cashier Dashboard"),
					"name": "Cashier Dashboard",
					"description": _("Cashier Dashboard"),
				},
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"label": _("Sales Invoice"),
					"description": _("View Invoices"),
				},
				{
					"type": "doctype",
					"name": "Journal Voucher",
					"label": _("Journal Voucher"),
					"description": _("Paid Entries"),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"label": _("Bundle Handling"),
					"description": _("All types of stock entry"),
				},
				{
					"type": "doctype",
					"name": "Attendance",
					"label": _("Attendance"),
					"description": _("Attendance"),
				},
			]
		},

		{
			"label": _("Reports"),
			"icon": "icon-star",
			"items": [
					{
					"type": "report",
					"is_query_report": True,
					"name": "Accounts Receivable",
					"doctype": "Sales Invoice"
					},
			]
		},
		
	]
