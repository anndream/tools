from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "page",
					"name": "admin-charts",
					"icon": "icon-sitemap",
					"label": _("Dashboard"),
					"link": "admin-charts",
					"description": _("Dashboard"),
				},
				{
					"type": "doctype",
					"name": "Admin Signature",
					"description": _("Admin Signature"),
				},
				{
					"type": "doctype",
					"name": "Pricing Rule",
					"label": _("Offer"),
					"description": _("List of offer"),
				},
			]
		},
		{
			"label": _("Setup"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Company",
					"description": _("Company Details"),
				},
				{
					"type": "doctype",
					"name": "Branch",
					"description": _("Branch Details"),
				},
				{
					"type": "doctype",
					"name": "Service",
					"description": _("List of Services"),
				},
				{
					"type": "doctype",
					"name": "Measurement",
					"description": _("List of Measurement"),
				},
				{
					"type": "doctype",
					"name": "Style",
					"description": _("Style"),
				},
				{
					"type": "doctype",
					"name": "Process",
					"description": _("List of Process"),
				},
				{
					"type": "doctype",
					"name": "Size",
					"description": _("Size"),
				},
				{
					"type": "doctype",
					"name": "Width",
					"description": _("Width"),
				},
			]
		},
	]
