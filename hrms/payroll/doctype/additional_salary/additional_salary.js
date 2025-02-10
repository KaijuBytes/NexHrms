// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Additional Salary", {
	setup: function (frm) {
		frm.add_fetch(
			"salary_component",
			"deduct_full_tax_on_selected_payroll_date",
			"deduct_full_tax_on_selected_payroll_date",
		);

		frm.set_query("employee", function () {
			return {
				filters: {
					agency: frm.doc.agency,
					status: ["!=", "Inactive"],
				},
			};
		});
	},

	onload: function (frm) {
		if (frm.doc.type) {
			frm.trigger("set_component_query");
		}
	},

	employee: function (frm) {
		if (frm.doc.employee) {
			frappe.run_serially([
				() => frm.trigger("get_employee_currency"),
				() => frm.trigger("set_agency"),
			]);
		} else {
			frm.set_value("agency", null);
		}
	},

	set_agency: function (frm) {
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Employee",
				fieldname: "agency",
				filters: {
					name: frm.doc.employee,
				},
			},
			callback: function (data) {
				if (data.message) {
					frm.set_value("agency", data.message.agency);
				}
			},
		});
	},

	agency: function (frm) {
		frm.set_value("type", "");
		frm.trigger("set_component_query");
	},

	set_component_query: function (frm) {
		if (!frm.doc.agency) return;
		let filters = { agency: frm.doc.agency };
		if (frm.doc.type) {
			filters.type = frm.doc.type;
		}
		frm.set_query("salary_component", function () {
			return {
				filters: filters,
			};
		});
	},

	get_employee_currency: function (frm) {
		frappe.call({
			method: "hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment.get_employee_currency",
			args: {
				employee: frm.doc.employee,
			},
			callback: function (r) {
				if (r.message) {
					frm.set_value("currency", r.message);
					frm.refresh_fields();
				}
			},
		});
	},

	salary_component: function (frm) {
		if (!frm.doc.ref_doctype) {
			frm.trigger("get_salary_component_amount");
		}
	},

	get_salary_component_amount: function (frm) {
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Salary Component",
				fieldname: "amount",
				filters: {
					name: frm.doc.salary_component,
				},
			},
			callback: function (data) {
				if (data.message) {
					frm.set_value("amount", data.message.amount);
				}
			},
		});
	},
});
