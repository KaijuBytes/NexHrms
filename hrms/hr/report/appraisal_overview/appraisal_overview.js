// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Appraisal Overview"] = {
	filters: [
		{
			fieldname: "agency",
			label: __("Agency"),
			fieldtype: "Link",
			options: "Agency",
			reqd: 1,
			default: frappe.defaults.get_user_default("Agency"),
		},
		{
			fieldname: "appraisal_cycle",
			fieldtype: "Link",
			label: __("Appraisal Cycle"),
			options: "Appraisal Cycle",
		},
		{
			fieldname: "employee",
			fieldtype: "Link",
			label: __("Employee"),
			options: "Employee",
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
		},
		{
			fieldname: "designation",
			label: __("Designation"),
			fieldtype: "Link",
			options: "Designation",
		},
	],
};
