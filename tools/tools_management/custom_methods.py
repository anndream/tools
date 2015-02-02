# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.widgets.reportview import get_match_cond
from frappe.utils import add_days, cint, cstr, date_diff, rounded, flt, getdate, nowdate, \
	get_first_day, get_last_day,money_in_words, now, nowtime
from frappe import _
from frappe.model.db_query import DatabaseQuery

def get_style(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select distinct style 
		from `tabStyle Item` where parent='%s'"""%(filters.get('item_code')))

def branch_methods(doc, method):
	branches_creation(doc)
	# territory_creation(doc)

def branches_creation(doc):
	if frappe.db.get_value('Branches', doc.branch, 'name') != doc.branch:
		br = frappe.new_doc('Branches')
		br.branch_name = doc.branch
		br.warehouse = doc.warehouse
		br.save(ignore_permissions=True)

def territory_creation(doc):
	if frappe.db.get_value('Territory', doc.branch, 'name')!= doc.branch:
		br = frappe.new_doc('Territory')
		br.territory_name = doc.branch
		br.is_group = 'No'
		br.save(ignore_permissions=True)		

def sales_invoice_on_submit_methods(doc, method):
	generate_project_aginst_si(doc, method)
	update_docstatus(doc)

def update_docstatus(doc):
	frappe.db.sql("update `tabSales Invoice Item` set docstatus=1 where parent='%s'"%(doc.name))	

def generate_project_aginst_si(doc, method):
	if not frappe.db.get_value('Project', doc.name, 'name'):
		pt = frappe.new_doc('Project')
		pt.project_name = doc.name
		pt.project_start_date = now()
		pt.save(ignore_permissions=True)
		generate_task(doc, method, pt.name)		

def generate_task(doc, method, name):
	for d in doc.get('entries'):
		if d.work_order:
			process_details = frappe.db.sql("select process from `tabWO Process` where parent='%s'"%(d.work_order))
			item_code = frappe.db.get_value('Work Order', d.work_order, 'item_code')
			if process_details:
				for process in process_details:
					create_task_against_process(doc,process[0], name, item_code)

def create_task_against_process(doc,process, name, item_code):
	if not frappe.db.get_value('Task',{'name':process,'project':name},'name') and item_code:
		c = frappe.new_doc('Task')
		c.subject = process + ' For Item ' + frappe.db.get_value('Item', item_code, 'item_name')
		c.process_name = process
		c.item_name = frappe.db.get_value('Item', item_code, 'item_name')
		c.sales_order_number = doc.name
		c.save()

def delete_project_aginst_si(doc, method):
	value = frappe.db.sql("select name from `tabTask` where sales_order_number='%s'"%(doc.name))
	if value:
		for d in value:
			frappe.db.sql("delete from `tabTime Log` where task='%s'"%(d[0]))
	frappe.db.sql("delete from `tabTask` where sales_order_number='%s'"%(doc.name))
	frappe.db.sql("delete from `tabProject` where name='%s'"%(doc.name))	

def merge_tailoring_items(doc,method):
	doc.set('entries', [])
	amt = amount = 0.0
	for d in doc.get('sales_invoice_items_one'):
		e = doc.append('entries', {})
		e.barcode=d.tailoring_barcode
		e.item_code=d.tailoring_item_code
		e.item_name=d.tailoring_item_name
		e.item_group = frappe.db.get_value('Item', d.tailoring_item_code, 'item_group')
		e.work_order=d.tailoring_work_order
		e.description=d.tailoring_description
		e.sales_invoice_branch = d.tailoring_branch
		e.warehouse= frappe.db.get_value('Branch', d.tailoring_branch, 'warehouse')
		e.income_account=d.tailoring_income_account
		e.cost_center=d.tailoring_cost_center
		e.batch_no=d.tailoring_batch_no
		e.item_tax_rate=d.tailoring_item_tax_rate
		e.stock_uom=d.tailoring_stock_uom 
		e.price_list_rate=d.tailoring_price_list_rate
		e.discount_percentage=d.tailoring_discount_percentage
		e.amount= d.tailoring_amount
		e.base_amount= cstr(flt(e.amount)*flt(doc.conversion_rate))
		e.base_rate=  cstr(flt(d.tailoring_rate)*flt(doc.conversion_rate))
		e.rate=d.tailoring_rate
		e.base_price_list_rate=d.tailoring_base_price_list_rate
		e.qty=d.tailoring_qty
		e.base_price_list_rate=d.tailoring_base_price_list_rate
		amt += flt(e.amount)
	amount = merge_merchandise_items(doc)
	doc.net_total_export = cstr(flt(amount) + flt(amt))
	doc.grand_total_export = cstr(flt(amount) + flt(amt) + flt(doc.other_charges_total_export))
	doc.rounded_total_export = cstr(rounded(flt(amount) + flt(amt) + flt(doc.other_charges_total_export)))
	doc.in_words_export = cstr(money_in_words(flt(amount) + flt(amt) + flt(doc.other_charges_total_export),doc.currency))
	doc.net_total = cstr(flt(doc.net_total_export) * flt(doc.conversion_rate))
	doc.grand_total = cstr(flt(doc.net_total) + flt(doc.other_charges_total))
	doc.rounded_total = cstr(rounded(flt(doc.net_total) + flt(doc.other_charges_total)))
	doc.in_words = cstr(money_in_words(flt(doc.net_total) + flt(doc.other_charges_total)))
	doc.outstanding_amount = cstr(flt(doc.net_total) + flt(doc.other_charges_total) - flt(doc.total_advance))
	return "Done"

def merge_merchandise_items(doc):
	amount = 0.0
	for d in doc.get('merchandise_item'):
		e = doc.append('entries', {})
		e.barcode=d.merchandise_barcode
		e.item_code=d.merchandise_item_code
		e.item_name=d.merchandise_item_name
		e.item_group = frappe.db.get_value('Item', d.merchandise_item_code, 'item_group')
		e.work_order=d.merchandise_work_order
		e.description=d.merchandise_description
		e.sales_invoice_branch = d.merchandise_branch
		e.warehouse = frappe.db.get_value('Branch', d.merchandise_branch, 'warehouse')
		e.income_account=d.merchandise_income_account
		e.cost_center=d.merchandise_cost_center
		e.batch_no=d.merchandise_batch_no
		e.item_tax_rate=d.merchandise_item_tax_rate
		e.stock_uom=d.merchandise_stock_uom 
		e.price_list_rate=d.merchandise_price_list_rate
		e.discount_percentage=d.merchandise_discount_percentage
		e.amount= d.merchandise_amount
		e.base_amount=cstr(flt(d.merchandise_amount)*flt(doc.conversion_rate))
		e.base_rate=cstr(flt(d.merchandise_rate)*flt(doc.conversion_rate))
		e.rate=d.merchandise_rate
		e.base_price_list_rate=d.merchandise_base_price_list_rate
		e.qty=d.merchandise_qty
		e.base_price_list_rate=d.merchandise_base_price_list_rate
		amount += flt(e.amount) 
	return amount

def get_item_details(doc, item):
	for d in doc.get('sales_invoice_items_one'):
		if d.tailoring_item_code == item:
			d.tailoring_item_name = frappe.db.get_value('Item', item, 'item_name')
			d.tailoring_description = frappe.db.get_value('Item', item, 'description')
			d.tailoring_stock_uom =frappe.db.get_value('Item', item, 'stock_uom')
			d.tailoring_rate = frappe.db.get_value('Item Price',{'price_list':d.tailoring_price_list,'item_code':item},'price_list_rate')
			d.tailoring_branch = frappe.db.get_value('Item', item, 'default_branch')
	return "Done"

def get_merchandise_item_details(doc, item):
	for d in doc.get('merchandise_item'):
		if d.merchandise_item_code == item:
			d.merchandise_item_name = frappe.db.get_value('Item', item, 'item_name')
			d.merchandise_description = frappe.db.get_value('Item', item, 'description')
			d.merchandise_stock_uom =frappe.db.get_value('Item', item, 'stock_uom')
			d.merchandise_rate = frappe.db.get_value('Item Price',{'price_list':d.merchandise_price_list,'item_code':item},'price_list_rate')
			d.merchandise_branch = frappe.db.get_value('Item', item, 'default_branch')
	return "Done"

@frappe.whitelist()
def get_styles_details(item, style):
	return frappe.db.sql("""select name,  ifnull(image_viewer, ''), ifnull(default_value,''), ifnull(abbreviation,''),
	ifnull(cost_to_customer,0.00), ifnull(cost_to_tailor,'') from `tabStyle Item`
		where parent='%s' and style='%s'"""%(item, style),as_list=1)

@frappe.whitelist()
def get_warehouse_wise_stock_balance(item, qty):
	fab_qty = []
	if item and qty:
		actual_qty = frappe.db.sql("""select  sle.warehouse, sle.actual_qty, b.branch from `tabBin` sle, `tabBranch` b 
				where sle.item_code = '%s'
					and b.warehouse = sle.warehouse"""%(item), as_list=1)

		co_qty = frappe.db.sql(""" select b.name, sum(fr.qty) from `tabFabric Reserve` fr, `tabBranch` b
       			where fr.fabric_code = '%s'
       				and fr.fabric_site = b.name and ifnull(fr.stock_entry_status , '') <> 'Completed'
      			group by b.name"""%item, as_list=1)

		if len(actual_qty)>0 and len(co_qty) > 0:
			for qty_detail in actual_qty:
				for co_detail in co_qty:
					if qty_detail[2] == co_detail[0]:
						if (flt(qty_detail[1]) - flt(co_detail[1])) > 0:
							fab_qty.append([ qty_detail[0], flt(qty_detail[1]) - flt(co_detail[1]), qty_detail[2]])
						actual_qty.remove(qty_detail)
		fab_qty.extend(actual_qty)
		return fab_qty

def update_work_order(doc, method):
	frappe.db.sql(""" update `tabWork Order` set sales_invoice_no = '%(sales_invoice_no)s' 
		where name in 
			(select tailor_work_order from `tabWork Order Distribution` 
				where parent = '%(sales_invoice_no)s') """%{'sales_invoice_no':doc.name})

def create_se_or_mr(doc, method):
	import json
	if doc.fabric_details:
		fabric_details = json.loads(doc.fabric_details)
		user_warehouse = get_user_branch()
		for item in fabric_details:
			warehouse_details = fabric_details.get(item)
			for warehouse in eval(warehouse_details):
				for item_details in eval(warehouse_details)[warehouse]:
					proc_warehouse = get_actual_fabrc_warehouse(doc.name, item_details[2])
					frappe.errprint([proc_warehouse, warehouse, user_warehouse])
					if proc_warehouse == warehouse and user_warehouse == warehouse:
						make_reserve_fabric_etry(1, doc, proc_warehouse, warehouse, item_details)
						# make_stock_transfer(proc_warehouse, warehouse, item_details[0], item_details[1])

					if proc_warehouse != warehouse and user_warehouse == warehouse:
						make_reserve_fabric_etry(2, doc, proc_warehouse, warehouse, item_details)
						# make_stock_transfer(proc_warehouse, warehouse, item_details[0], item_details[1])

					if proc_warehouse != warehouse and user_warehouse != warehouse:
						make_reserve_fabric_etry(doc.name, proc_warehouse, warehouse, item_details)

def cut_order_generation(work_order, invoice_no):
	item = get_wo_item(work_order)
	if not check_cut_order_exist(invoice_no, item):
		fabric_details = get_fabric_info(invoice_no)
		user_warehouse = get_user_branch()
		if fabric_details:
			warehouse_details = eval(fabric_details.get(item))
			for warehouse in warehouse_details:
				for item_details in warehouse_details[warehouse]:
					proc_warehouse = get_actual_fabrc_warehouse(invoice_no, item_details[2])
					
					if proc_warehouse == warehouse and user_warehouse == warehouse:
						make_cut_order(1, invoice_no, proc_warehouse, warehouse, item_details)
						# make_stock_transfer(proc_warehouse, warehouse, item_details[0], item_details[1])

					if proc_warehouse != warehouse and user_warehouse == warehouse:
						make_cut_order(2, invoice_no, proc_warehouse, warehouse, item_details)
						# make_stock_transfer(proc_warehouse, warehouse, item_details[0], item_details[1])

					if proc_warehouse != warehouse and user_warehouse != warehouse:
						# make_material_request(doc.name, proc_warehouse, warehouse, item_details[0], item_details[1])
						make_cut_order(2, invoice_no, proc_warehouse, warehouse, item_details)

def get_wo_item(work_order):
	return frappe.db.get_value('Work Order', work_order, 'item_code')

def check_cut_order_exist(invoice_no, item_code):
	return frappe.db.get_value('Cut Order', {'invoice_no': invoice_no, 'article_code': item_code}, 'name')

def get_fabric_info(invoice_no):
	frappe.errprint(invoice_no)
	fabric_details = frappe.db.get_value("Sales Invoice", invoice_no, 'fabric_details')

	if fabric_details:
		return eval(fabric_details)
	
	return None

def get_actual_fabrc_warehouse(si, item):
	ret = frappe.db.sql("""select warehouse from `tabProcess Wise Warehouse Detail` 
					where parent = ( select name from `tabWork Order` 
						where sales_invoice_no = '%s' and item_code = '%s') 
					and ifnull(actual_fabric, 0) = 1"""%(si, item), as_list=1, debug=1)

	if ret:
		return ret[0][0]
	# Rohit Newly added Code
	else:
		data = frappe.db.sql("""select warehouse from `tabProcess Wise Warehouse Detail` 
					where parent = ( select name from `tabWork Order` 
						where sales_invoice_no = '%s' and item_code = '%s') order by name desc limit 1"""%(si, item), as_list=1, debug=1)
		if data:
			return data[0][0]

def get_user_branch():
	return frappe.db.get_value("User", frappe.session.user, "branch")
	# ret = frappe.db.sql(""" select warehouse from tabBranch b, tabUser u 
	# 	where b.name = u.branch and u.name = '%s' """%(frappe.session.user), as_list=1)

	# return ((len(ret[0]) > 1 ) and ret[0] or ret[0][0]) if ret else None	

def make_stock_transfer(proc_warehouse, warehouse, fabric, qty):
	fab_details = get_fabric_details(fabric)
	
	se = frappe.new_doc('Stock Entry')
	se.naming_series =  get_series("Stock Entry")
	se.purpose_type = 'Material Out'
	se.purpose = 'Material Issue'
	se.branch = frappe.db.get_value('User', frappe.session.use, 'branch')
	se.posting_date = nowdate()
	se.posting_time = nowtime().split('.')[0]
	
	sed = se.append('mtn_details', {})
	sed.s_warehouse = get_warehouse(warehouse)
	sed.target_branch = proc_warehouse
	sed.item_code = fabric
	sed.item_name = fab_details.get('item_name')
	sed.description = fab_details.get('description')
	sed.qty = qty
	sed.stock_uom = fab_details.get('stock_uom')
	sed.uom = fab_details.get('stock_uom')
	sed.conversion_factor = 1
	sed.incoming_rate = 0.0
	sed.transfet_qty = qty * 1

	se.save()

def get_series(doctype):
	return frappe.get_meta(doctype).get_field("naming_series").options or ""

def get_fabric_details(fabric):
	return frappe.db.get_value('Item', fabric,['item_name', 'description', 'stock_uom'], as_dict=1)

def get_branch(proc_warehouse):
	return frappe.db.get_value('Branch', {'warehouse': proc_warehouse}, 'name')

def make_material_request(si_no, proc_warehouse, warehouse, fabric, qty):
	fab_details = get_fabric_details(fabric)
	
	mrq = frappe.new_doc('Material Request')
	mrq.naming_series =  get_series("Material Request")
	mrq.material_request_type = 'Transfer'
	# mrq.branch = frappe.db.get_value('User', frappe.session.use, 'branch')
	
	mrqd = mrq.append('indent_details', {})
	mrqd.invoice_no = si_no
	mrqd.for_branch = proc_warehouse 
	mrqd.from_branch = warehouse
	mrqd.warehouse = get_warehouse(proc_warehouse)
	mrqd.from_warehouse = get_warehouse(warehouse)
	mrqd.item_code = fabric
	mrqd.item_name = fab_details.get('item_name')
	mrqd.description = fab_details.get('description')
	mrqd.qty = qty
	mrqd.uom = fab_details.get('stock_uom')
	mrqd.schedule_date = add_days(nowdate(), 2)

	mrq.save(ignore_permissions=True)

def get_warehouse(branch):
	return frappe.db.get_value('Branches', branch, 'warehouse')

def make_cut_order(id, invoice_no, proc_warehouse, warehouse, item_details, mr_view=None):
	co = frappe.new_doc("Cut Order")
	co.invoice_no = invoice_no
	co.article_code = item_details[2]
	co.fabric_code = item_details[0]
	co.qty = item_details[1]
	co.actual_site = proc_warehouse
	co.fabric_site = warehouse
	if mr_view:
		co.submit()
	else:
		co.save()

def make_reserve_fabric_etry(id, doc, proc_warehouse, warehouse, item_details, mr_view=None):
	frappe.errprint([id,"test"])
	co = frappe.new_doc("Fabric Reserve")
	co.invoice_no = doc.get('name')
	co.article_code = item_details[2]
	co.fabric_code = item_details[0]
	co.qty = item_details[1]
	co.actual_site = proc_warehouse
	co.fabric_site = warehouse
	if mr_view:
		co.submit()
	else:
		co.save()

def get_branch_of_process(doctype, txt, searchfield, start, page_len, filters):
	branch = []
	try:
		data = frappe.db.sql(""" Select branch_list from `tabProcess Item` where 
			process_name = '%s' and parent ='%s'"""%(filters.get('process'), filters.get('item_code')), as_list=1, debug=1)
		if data:
			for s in data:
				serial = (s[0]).split('\n')
				for sn in serial:
					branch.append([sn])
			return branch
		else:
			return frappe.db.sql("select name from `tabBranch`")
	except Exception:
		return frappe.db.sql("select name from `tabBranch`")

def get_serial_no(doctype, txt, searchfield, start, page_len, filters):
	serial_no =[]
	txt = "%{}%".format(txt)
	try:
		if filters.get('serial_no'):
			sn = cstr(filters.get('serial_no')).split('\n')
			for s in sn:
				serial_no.append([s])
			return serial_no
		else:
			return frappe.db.sql("select name from `tabSerial No` where %s like '%s'"%(searchfield, txt))
	except Exception:
		return frappe.db.sql("select name from `tabSerial No` where %s like '%s'"%(searchfield, txt))

def get_process_details(doctype, txt, searchfield, start, page_len, filters):
	obj = eval(filters.get('obj'))
	obj_list = "','".join(obj)
	if obj_list:
		return frappe.db.sql("""select name from `tabProcess` where name in ('%s')"""%(obj_list))
	else:
		return frappe.db.sql("""select name from `tabProcess`""")

def get_unfinished_process(doctype, txt, searchfield, start, page_len, filters):
	cond = "1=1"
	if filters.get('get_finished_list'):
		cond = "name not in ('%s')"%(filters.get('get_finished_list'))
	return frappe.db.sql("""select distinct process_name from `tabProcess Item` 
		where parent = '%s' and trials = 1 and %s"""%(filters.get('item_code'), cond))


def validate_reserve_fabric(doc, method):
	import json
	data = json.loads(doc.fabric_details)
	# if data:
	tailoring_data = doc.get('sales_invoice_items_one')
	reserve_fab_list = []
	if tailoring_data:
		for s in data:
			reserve_fab_list.append(s)
		data_dict = reserve_fabric_for_UnreserveItem(tailoring_data, reserve_fab_list, data)
		doc.fabric_details = json.dumps(data_dict)
	return True

def reserve_fabric_for_UnreserveItem(tailoring_data, reserve_fab_list, data):
	import json
	for args in tailoring_data:
		if args.tailoring_item_code not in reserve_fab_list:
			if args.fabric_code:
				if args.fabric_qty:
					qty = get_fabric_Available_qty(args.fabric_code, args.tailoring_item_code, args.fabric_qty)
					data[args.tailoring_item_code] = json.dumps(qty)
				else:
					frappe.throw(_("Fabric qty is not selected for item {0}").format(args.tailoring_item_code))	
			else:
				frappe.throw(_("Fabric is not selected for item {0}").format(args.tailoring_item_code))
	return data

def get_fabric_Available_qty(fabric_code, item_code, fab_qty):
	warehouse= get_branch_warehouse(get_user_branch())
	inner_list ={}
	qty_data = frappe.db.sql(""" select item_code, %s as qty from `tabBin`
		where item_code = '%s' and warehouse='%s' and actual_qty>=%s"""%(fab_qty, fabric_code, warehouse, fab_qty), as_list=1)
	if qty_data:
		qty_data[0].append(item_code)
		inner_list[get_user_branch()] = qty_data
		return inner_list
	else:
		frappe.throw(_("Fabric is not reserved for item {0}").format(item_code))

def get_branch_warehouse(branch):
	return frappe.db.get_value('Branch', branch, 'warehouse')
