from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Request Of Tools",
					"description": _("Request Of Tools"),
				},
				{
					"type": "doctype",
					"name": "Tools Allocation",
					"label": _("Tools Allocation"),
					"description": _("Tools Allocation"),
				},
				{
					"type": "doctype",
					"name": "Tool Maintenance",
					"label": _("Tool Maintenance"),
					"description": _("Tool Maintenance"),
				},
			]
		},
		
	]
