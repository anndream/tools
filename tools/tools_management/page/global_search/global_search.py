import frappe
import itertools

@frappe.whitelist()
def get_result_set(search_string):
	return{
		'sales': get_sales(search_string),
		'purchase': get_purchase(search_string),
		'inventory': get_inventory(search_string)
	}

def get_sales(search_string):
	sales = []
	get_cust(search_string, sales)
	get_sales_invoice(search_string, sales)
	return sales

def get_cust(search_string, sales):
	cust = frappe.db.sql(""" select concat('<a href="#Form/Customer/',name,'">', name, '</a>', '<br> Customer <br>' ) from tabCustomer 
		where customer_name like '%%%(search_string)s%%' 
		or customer_type like '%%%(search_string)s%%' or customer_group like '%%%(search_string)s%%' """%{'search_string':search_string}, as_list=1)
	sales.extend(cust)

def get_sales_invoice(search_string, sales):
	si = frappe.db.sql(""" select concat('Invoice No <a href="#Form/Sales Invoice/',si.name,'">', si.name, '</a> was booked on  ',si.posting_date,'    ',
		    "<br>Customer Name :<a href='#Form/Customer/" , si.customer,"'>",si.customer,'</a>'
		    '<br> Total Advance : ', si.total_advance,'<br> Outstanding : ', si.outstanding_amount,'<br> Total : ', si.rounded_total_export) 
		from `tabSales Invoice` si, `tabSales Invoice Item` sii
		where (si.customer like '%%%(search_string)s%%' )
			or ( sii.barcode like '%%%(search_string)s%%'
			or sii.item_code like '%%%(search_string)s%%'
			or sii.item_name like '%%%(search_string)s%%'
			or si.name like '%%%(search_string)s%%')
			and sii.parent = si.name
			group by si.name
			"""%{'search_string': search_string})
	sales.extend(si)

def get_purchase(search_string):
	purchase = []
	supplier = get_supllier(search_string, purchase)
	po = get_purchase_order(search_string, purchase)
	pi = get_purchase_invoice(search_string, purchase)
	return purchase

def get_supllier(search_string, purchase):
	supplier = frappe.db.sql(""" select concat('<a href="#Form/Supplier/',name,'">', name, '</a>', '<br> Supplier <br>' ) from tabSupplier 
		where supplier_name like '%%%(search_string)s%%' 
		or supplier_type like '%%%(search_string)s%%'"""%{'search_string':search_string}, as_list=1)
	purchase.extend(supplier)	

def get_purchase_invoice(search_string, purchase):
	pi = frappe.db.sql(""" select concat('<a href="#Form/Purchase Invoice/',pi.name,'">', pi.name, '</a>',
		'<br> Total Advance', pi.total_advance,'<br> Outstanding ', pi.outstanding_amount,'<br> Total', pi.total_amount_to_pay) 
		from `tabPurchase Invoice` pi, `tabPurchase Invoice Item` pii
		where (pi.supplier like '%%%(search_string)s%%' )
			or (pii.item_code like '%%%(search_string)s%%'
			or pii.item_name like '%%%(search_string)s%%'
			and pii.parent = pi.name)
			"""%{'search_string': search_string},as_list=1)
	purchase.extend(pi)	

def get_purchase_order(search_string, purchase):
	po = frappe.db.sql(""" select concat('<a href="#Form/Purchase Order/',po.name,'">', po.name, '</a>',
		'<br> Total', po.grand_total_import) 
		from `tabPurchase Order` po, `tabPurchase Order Item` poi
		where (po.supplier like '%%%(search_string)s%%' )
			or (poi.item_code like '%%%(search_string)s%%'
			or poi.item_name like '%%%(search_string)s%%'
			and poi.parent = po.name)
			"""%{'search_string': search_string},as_list=1)
	purchase.extend(po)	

def get_inventory(search_string):
	inventory = []
	item = get_item(search_string, inventory)
	pr = get_purchase_receipt(search_string, inventory)
	dn = get_delivery_note(search_string, inventory)
	# se = get_stock_entry(search_string, inventory)
	sn = get_serial_no(search_string, inventory)
	return inventory

def get_item(search_string, inventory):
	item = frappe.db.sql(""" select concat('<a href="#Form/Item/',name,'">', name, '</a>', '<br> Item <br>' ) from tabItem 
		where item_code like '%%%(search_string)s%%' 
		or item_name like '%%%(search_string)s%%'
		or description like '%%%(search_string)s%%'
		or stock_uom like '%%%(search_string)s%%'
		or brand like '%%%(search_string)s%%'
		or barcode like '%%%(search_string)s%%'"""%{'search_string':search_string}, as_list=1)
	inventory.extend(item)

def get_purchase_receipt(search_string, inventory):
	pr = frappe.db.sql("""select concat('<a href="#Form/Purchase Receipt/',pr.name,'">', pr.name, '</a>',
		'<br> Total', pr.grand_total_import) 
		from `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pri
		where (pr.supplier like '%%%(search_string)s%%'  )
			or (pri.item_code like '%%%(search_string)s%%' 
			or pri.item_name like '%%%(search_string)s%%' 
			or pri.serial_no like '%%%(search_string)s%%' 
			and pri.parent = pr.name) """%{'search_string':search_string}, as_list=1)
	inventory.extend(pr)

def get_delivery_note(search_string, inventory):
	dn = frappe.db.sql("""select concat('<a href="#Form/Delivery Note/',dn.name,'">', dn.name, '</a>',
		'<br> Total', dn.grand_total_export) 
		from `tabDelivery Note` dn, `tabDelivery Note Item` dni
		where (dn.customer like '%%%(search_string)s%%' )
			or (dni.item_code like '%%%(search_string)s%%'
			or dni.item_name like '%%%(search_string)s%%'
			or dni.serial_no like '%%%(search_string)s%%'
			and dni.parent = dn.name)"""%{'search_string':search_string}, as_list=1)
	inventory.extend(dn)

def get_stock_entry(search_string, inventory):
	se = frappe.db.sql("""select concat('<a href="#Form/Stock Entry/',se.name,'">', se.name, '</a>') 
		from `tabStock Entry` se, `tabStock Entry Detail` sed
		where (sed.item_code like '%%%(search_string)s%%'
			or sed.item_name like '%%%(search_string)s%%'
			or sed.serial_no like '%%%(search_string)s%%'
			and sed.parent = se.name)"""%{'search_string':search_string}, as_list=1)
	inventory.extend(se)

def get_serial_no(search_string,inventory):
	data = frappe.db.sql(""" select name from `tabSerial No` where name like '%%%(search_string)s%%'"""%{'search_string':search_string}, as_list=1)
	if data:
		for serial_no in data:
			sn = frappe.db.sql(""" SELECT
		    concat('Serial No : ', '<a href="#Form/Serial No/',sno.name,'">', sno.name, '</a>',"<br>Item Code  : ",sno.item_code,"<br>Item Name  : ",item_name,"<br>Item Description  : ",description,"<br>Current Process  : ",ifnull
		    (snd.process,''),"<br>Process Status : ",
		    CASE
		        WHEN wo.status !='Release'
		        THEN 'Pending'
		        WHEN sno.completed='Yes'
		        THEN 'Completed'
		        ELSE ifnull(snd.status,'Under Manufacturing Process')
		    END,"<br>Product Status : ",
		    CASE
		        WHEN wo.status !='Release'
		        THEN 'Work Order Not Release'
		        WHEN sno.status='Delivered'
		        THEN sno.status
		        WHEN sno.completed='Yes'
		        THEN 'Product is ready for delivery'
		        ELSE 'Product is not ready to deliver'
		    END,"<br>Trial No : ", ifnull(snd.trial_no,'No'),    
		    CASE
		        WHEN snd.has_qc=1
		        THEN concat("<br>QC Status :",ifnull(snd.qc_completed,'Incomplete'))
		        ELSE ''
		    END,'<br>Warehouse :', ifnull(sno.warehouse,''), 
		    '<br>Sales Invoice: ', '<a href="#Form/Sales Invoice/',sno.sales_invoice,'">',sno.sales_invoice,'</a>' ,'<br>Work Order: ', '<a href="#Form/Work Order/',sno.work_order,'">',sno.work_order, '</a>')
		FROM
		    `tabSerial No` sno
		LEFT JOIN
		    `tabSerial No Detail` snd
		ON
		    snd.parent= sno.name
		LEFT JOIN
		    `tabWork Order` wo
		ON
		    wo.name = sno.work_order
				WHERE
				    sno.name = '%s'
				ORDER BY
				    snd.creation DESC limit 1 """%(serial_no[0]),as_list=1)
			inventory.extend(sn)    
