frappe.pages['global-search'].onload = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Global search',
		single_column: true
	});

	$(wrapper).find(".layout-main").html("<div class='user-settings'></div>\
			<table class='table table-condensed'>\
					<tr style='width:100%;'>\
						<td ><div class='search_field' ></div></td>\
						<td><div id ='search_area' style='padding-left:40px'><button class='btn btn-info' padding-top='0'>"+__('Search')+"</button></div></td>\
						<td><div><button class='btn btn-info' id='qrcode' style='padding-left:30px' padding-top='0'>"+__('Qrcode Scanner')+"</button></div></td>\
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
		this.init_for_qr_code_scanner()
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

	},
	init_for_qr_code_scanner:function(){
		var me = this
		$('#qrcode').click(function(){
				me.render_qrcode_scanner()
			})

	},
	render_qrcode_scanner:function(){
		this.dialog = new frappe.ui.Dialog({
			width:900,
			title:__('Qrcode Scanner'),
			fields: [
				{fieldtype:'HTML', fieldname:'qrcode_html', label:__('Styles'), reqd:false,
					description: __(""),options:'<div id="my_div" style="max-width:900px"><div>'}
			]
		})

		this.fd = this.dialog.fields_dict;
		this.render_dialog()

	},
	render_dialog:function(){
		$('<div id="QR-Code" class="container" style="width:100%">\
		<div class="panel panel-primary">\
		<div class="panel-heading" style="display: inline-block;width: 100%;">\
		<h4 style="width:50%;float:left;"></h4>\
		<div style="width:50%;float:right;margin-top: 5px;margin-bottom: 5px;text-align: right;">\
		<select id="cameraId" class="form-control" style="display: inline-block;width: auto;"></select>\
		<button id="save" data-toggle="tooltip" title="Image shoot" type="button" class="btn btn-info btn-sm disabled"><span class="glyphicon glyphicon-picture"></span></button>\
		<button id="play" data-toggle="tooltip" title="Play" type="button" class="btn btn-success btn-sm"><span class="glyphicon glyphicon-play"></span></button>\
		<button id="stop" data-toggle="tooltip" title="Stop" type="button" class="btn btn-warning btn-sm"><span class="glyphicon glyphicon-stop"></span></button>\
		<button id="stopAll" data-toggle="tooltip" title="Stop streams" type="button" class="btn btn-danger btn-sm"><span class="glyphicon glyphicon-stop"></span></button>\
		</div>\
		</div>\
		<div class="panel-body">\
		<div class="col-md-6" style="text-align: center;">\
		<div class="well" style="position: relative;display: inline-block;">\
		<canvas id="qr-canvas" width="320" height="240"></canvas>\
		<div class="scanner-laser laser-rightBottom" style="opacity: 0.5;"></div>\
		<div class="scanner-laser laser-rightTop" style="opacity: 0.5;"></div>\
		<div class="scanner-laser laser-leftBottom" style="opacity: 0.5;"></div>\
		<div class="scanner-laser laser-leftTop" style="opacity: 0.5;"></div>\
		</div>\
		<div class="well"  id="tools" style="position: relative;" >\
		<label id="zoom-value" width="100">Zoom: 2</label>\
		<input type="range" id="zoom" value="20" min="10" max="30" onchange="Page.changeZoom();"/>\
		<label id="brightness-value" width="100">Brightness: 0</label>\
		<input type="range" id="brightness" value="0" min="0" max="128" onchange="Page.changeBrightness();"/>\
		<label id="contrast-value" width="100">Contrast: 0</label>\
		<input type="range" id="contrast" value="0" min="0" max="64" onchange="Page.changeContrast();"/>\
		<label id="threshold-value" width="100">Threshold: 0</label>\
		<input type="range" id="threshold" value="0" min="0" max="512" onchange="Page.changeThreshold();"/>\
		<label id="sharpness-value" width="100">Sharpness: off</label>\
		<input type="checkbox" id="sharpness" onchange="Page.changeSharpness();"/>\
		<label id="grayscale-value" width="100">grayscale: off</label>\
		<input type="checkbox" id="grayscale" onchange="Page.changeGrayscale();"/>\
		</div>\
		</div>\
		<div class="col-md-6" style="text-align: center;">\
		<div id="result" class="thumbnail">\
		<div class="well" style="position: relative;display: inline-block;">\
		<img id="scanned-img" src="" width="320" height="240">\
		</div>\
		<div class="caption">\
		<h3>Scanned result</h3>\
		<p id="scanned-QR"></p>\
		</div>\
		</div>\
		</div>\
		<p style="text-align:center"><button id="search_qr_result"  class="btn btn-primary" style>Search Qrcode Result</button>\
		</div>\
		<div class="panel-footer">\
		</div>\
		</div>\
		</div>').appendTo($(this.fd.qrcode_html.wrapper).find('#my_div'))
		$('.modal-dialog').css({"width":"900px","height":"600px"})
		$(this.fd.qrcode_html.wrapper).find('#tools').css("display","None")
		$(this.fd.qrcode_html.wrapper).find('#cameraId').css("display","None")
		this.dialog.show()

		frappe.require("assets/js/qrcodelib.js");
		frappe.require("assets/js/WebCodeCam.js");
		frappe.require("assets/js/main.js");
		frappe.require("assets/css/qrcode.css");

		this.search_with_qrcode_result()
		  
	},
	search_with_qrcode_result:function(){
		var me = this
		$(me.fd.qrcode_html.wrapper).find('#search_qr_result').click(function(){
			if ($(me.fd.qrcode_html.wrapper).find('#scanned-QR').text()){
				$('[data-fieldname="search_string"]').val($('#scanned-QR').text())
				me.dialog.hide()
				$(me.fd.qrcode_html.wrapper).empty()
				me.get_reult()
			}else{
				alert("Scanned Result is Empty")
			}
			
		})
	}



})