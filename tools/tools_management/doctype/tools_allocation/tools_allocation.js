// cur_frm.cscript.onload= function(doc, cdt, cdn) {
// 	// console.log("serial_no");
// 	var d = locals[cdt][cdn]
//     get_server_fields('get_details',d.purpose,'',doc, cdt, cdn, 1 , function(doc, cdt, cdn){
//      refresh_field('tools_info');
//      });

// };

cur_frm.cscript.add= function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	console.log("in the add")
	d.serial_nos=d.serial_no;
	refresh_field('serial_nos',d.name,'tools_info');
};

cur_frm.cscript.purpose= function(doc, cdt, cdn) {
	// console.log("serial_no");
	var d = locals[cdt][cdn]
    get_server_fields('get_details',d.purpose,'',doc, cdt, cdn, 1 , function(doc, cdt, cdn){
     refresh_field('tools_info');
     });

};

cur_frm.cscript.serial_no = function(doc, cdt, cdn){
	console.log("serial_no");
    var d = locals[cdt][cdn]
    get_server_fields('check_availabilty',d.serial_no,'',doc, cdt, cdn, 1 , function(doc, cdt, cdn){
   });
};
