cur_frm.cscript.parameter =function(doc,cdt,cdn){
var d = locals[cdt][cdn]
get_server_fields('get_details',d.parameter,'',doc, cdt, cdn, 1 ,function(){
refresh_field('measurement_table')
})
}
