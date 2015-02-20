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
					"icon": "icon-dashboard",
					"description": _("Cashier Dashboard"),
				},
				{
					"type": "doctype",
					"name": "Cut Order Dashboard",
					"label": _("Cut Order Dashboard"),
					"description": _("Cut Order Dashboard"),
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
				{
					"type": "page",
					"name": "production-forecast",
					"icon": "icon-bullseye",
					"label": _("Production Forecast"),
					"link": "production-forecast",
					"description": _("Production Forecast"),
				},
			]
		},

		{
			"label": _("Reports"),
			"icon": "icon-list",
			"items": [
					{
					"type": "report",
					"name":"General Ledger",
					"doctype": "GL Entry",
					"is_query_report": True,
					"icon":"icon-file-text"
					},
					{
					"type": "report",
					"is_query_report": True,
					"name": "Accounts Receivable",
					"doctype": "Sales Invoice"
					},
					{
					"type": "page",
					"name": "sales-analytics",
					"label": _("Sales Analytics"),
					"icon": "icon-bar-chart",
					},
					{
						"type": "page",
						"name": "sales-funnel",
						"label": _("Sales Funnel"),
						"icon": "icon-bar-chart",
					},
					{
						"type": "report",
						"is_query_report": True,
						"name": "Customer Acquisition and Loyalty",
						"doctype": "Customer",
						"icon": "icon-bar-chart",
					},
			]
		},
		
	]
