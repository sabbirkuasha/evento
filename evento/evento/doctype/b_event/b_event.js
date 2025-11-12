// Copyright (c) 2025, sabbir.kuasha@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("B Event", {
	refresh(frm) {
		frappe.call("frappe.geo.country_info.get_country_timezone_info")
		.then(({message})=> {
			frm.set_df_property("time_zone", "options", message.all_timezones)
			.catch(() => frappe.msgprint(__("Could not fetch time zones")));;
		})
	},
});
