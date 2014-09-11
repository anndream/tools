cur_frm.cscript.view_image = function(doc, cdt, cdn) {
doc.user_image_show = '<table style="width: 100%; table-layout: fixed;"><tr><td><img src="'+doc.view_image+'" width="100px"></td></tr></table>'
refresh_field("user_image_show");
}
