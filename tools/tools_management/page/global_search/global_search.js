frappe.pages['global-search'].onload = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Global search',
		single_column: true
	});

	$(wrapper).find(".layout-main").html("<div class='user-settings'></div>\
			<table class='table table-condensed'>\
					<tr style='width:100%;'>\
						<td colspan='2'><div class='search_field' ></div></td>\
						<td><div id ='search_area' ><button class='btn btn-info' padding-top='0'>"+__('Search')+"</button></div></td>\
					</tr>\
					<tr style='width:100%;' id = 'result_tr'>\
					</tr>\
					<tr style='width:100%;' id = 'result_span'>\
					</tr>\
			</table>")
	wrapper.search_details = new frappe.GlobalSearch(wrapper);
}

frappe.GlobalSearch =  Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.make();
	},
	make: function(){
		this.create_search_area()
		// this.data = [['Saurabh'],['Saurabh1'],['Saurabh2'],['Saurabh3'],['Saurabh4'],['Saurabh5'],['Saurabh6'],['Saurabh7'],['Saurabh8'],['Saurabh9'],['Saurabh10']]
		this.data = {};
	},
	create_search_area: function(){
		var me = this;
		this.search_str = frappe.ui.form.make_control({
				df: {
					"fieldtype": 'Data',
					"fieldname": "search_string",
					"placeholder":"Search String"
				},
				parent:$('.search_field'),
			});
		this.search_str.make_input();
		$('#search_area').click(function(){
				me.get_reult()
			})
	},
	get_reult: function(){
		var me = this;
		frappe.call({
			method:"tools.tools_management.page.global_search.global_search.get_result_set",
			args:{'search_string': me.search_str.$input.val()},
			callback:function(r){
				me.data['Sales']= r.message.sales
				me.data['Purchase']= r.message.purchase
				me.data['Inventory']= r.message.inventory
				me.render_result_tr()
			}
		})
		// this.render_result_tr()
	},
	render_result_tr: function(){
		var me = this;
		this.pos_dict = {};
		this.div_dict = {};
		$('#result_tr').empty()
		$('#result_span').empty()
		columns = [["Sales<i class='icon-angle-down'></i>", 33], ["Purchase",33], ["Inventory", 33]];

		$.each(columns, 
			function(i, col) {
			$("<th>").html(col[0]).css("width", col[1]+"%")
				.appendTo($('#result_tr')).click(function(){
					div_id = $(this)[0].innerText;
					if($('#'+div_id).hasClass("in"))  {
						$('#'+div_id).collapse('hide')
					}
					else{
						$('#'+div_id).collapse('show');
					}
				});
		});

		res_div = [['<div id = "Sales"  class="collapse in">Test Sales</div>',33],['<div id = "Purchase" class="collapse in">Test Purchase</div>',33],
			['<div id = "Inventory" class="collapse in">Test Inventory</div>',33]]
		$.each(res_div, 
			function(i, col) {
			$("<td>").html(col[0]).css("width", col[1]+"%")
				.appendTo($('#result_span'));
		});
		$.each([['Sales'],['Purchase'],['Inventory']], function(i,col){
			me.render_result_table(col[0], me.data[col[0]].slice(0,5))
		})
	},
	render_result_table: function(div_id, data){
		var me = this;
		$('#'+div_id).empty();
		var prev = 0;
		var next = 5;
		this.div_dict[div_id] = $("<table class='table table-bordered'>\
			<thead><tr></tr></thead>\
			<tbody></tbody>\
		</table>").appendTo('#'+div_id);

		$.each([['<',5],[__("Search Data"), 100],['>',5]],
			function(i, col) {
			var td_id = div_id + "_"+col[0]
			$("<th id = '"+td_id+"'>").html(col[0]).css("width", col[1]+"%")
				.appendTo(me.div_dict[div_id].find("thead tr")).click(function(){
					me.render_next_results_set($(this), div_id)
				});
		});
		this.render_result(data.slice(prev,next), prev, next, div_id)
	},
	render_result: function(data, prev, next, div_id){
		var me = this;
		$.each(data, function(i, d) {
			var row = $("<tr>").appendTo(me.div_dict[div_id].find("tbody"));
			$("<td colspan='3'>").html(d[0]).appendTo(row);
			if(!me.pos_dict[div_id]){
				me.pos_dict[div_id] = {}	
			}
			me.pos_dict[div_id]['prev'] = prev;
			me.pos_dict[div_id]['next'] = next;
		});
	},
	render_next_results_set: function(btn, div_id){
		var me = this;
		div_id = btn[0].id.split('_')[0]
		this.div_dict[div_id].find("tbody").empty()
		prev = me.pos_dict[div_id]['prev']
		next = me.pos_dict[div_id]['next']
		if(btn[0].innerText == '<'){
			if(prev!=0){
				this.render_result(this.data[div_id].slice(prev-5,next-5), prev-5, next-5, div_id)
			}
		}
		if(btn[0].innerText == '>'){
			if(next!=this.data.length){
				this.render_result(this.data[div_id].slice(prev+5,next+5), prev+5, next+5, div_id)
			}
		}

	}
})