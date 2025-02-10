// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Bank Remittance"] = {
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
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
		},
	],
};
