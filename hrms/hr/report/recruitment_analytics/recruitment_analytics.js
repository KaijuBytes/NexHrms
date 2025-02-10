// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Recruitment Analytics"] = {
	filters: [
		{
			fieldname: "agency",
			label: __("Agency"),
			fieldtype: "Link",
			options: "Agency",
			default: frappe.defaults.get_user_default("Agency"),
			reqd: 1,
		},
		{
			fieldname: "on_date",
			label: __("On Date"),
			fieldtype: "Date",
			default: frappe.datetime.now_date(),
			reqd: 1,
		},
	],
};
