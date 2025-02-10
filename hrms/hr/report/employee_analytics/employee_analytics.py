# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}

	if not filters["agency"]:
		frappe.throw(_("{0} is mandatory").format(_("Agency")))

	columns = get_columns()
	employees = get_employees(filters)
	parameters_result = get_parameters(filters)
	parameters = []
	if parameters_result:
		for department in parameters_result:
			parameters.append(department)

	chart = get_chart_data(parameters, employees, filters)
	return columns, employees, None, chart


def get_columns():
	return [
		_("Employee") + ":Link/Employee:120",
		_("Name") + ":Data:200",
		_("Date of Birth") + ":Date:100",
		_("Branch") + ":Link/Branch:120",
		_("Department") + ":Link/Department:120",
		_("Designation") + ":Link/Designation:120",
		_("Gender") + "::100",
		_("Agency") + ":Link/Agency:120",
	]


def get_conditions(filters):
	conditions = " and " + filters.get("parameter").lower().replace(" ", "_") + " IS NOT NULL "

	if filters.get("agency"):
		conditions += " and agency = '%s'" % filters["agency"].replace("'", "\\'")
	return conditions


def get_employees(filters):
	conditions = get_conditions(filters)
	# nosemgrep: frappe-semgrep-rules.rules.frappe-using-db-sql
	return frappe.db.sql(
		"""select name, employee_name, date_of_birth,
	branch, department, designation,
	gender, agency from `tabEmployee` where status = 'Active' %s"""
		% conditions,
		as_list=1,
	)


def get_parameters(filters):
	if filters.get("parameter") == "Grade":
		parameter = "Employee Grade"
	else:
		parameter = filters.get("parameter")

	return frappe.db.sql("""select name from `tab""" + parameter + """` """, as_list=1)


def get_chart_data(parameters, employees, filters):
	if not parameters:
		parameters = []
	datasets = []
	parameter_field_name = filters.get("parameter").lower().replace(" ", "_")
	label = []
	for parameter in parameters:
		if parameter:
			total_employee = frappe.db.sql(
				"""select count(*) from
				`tabEmployee` where """
				+ parameter_field_name
				+ """ = %s and  agency = %s""",
				(parameter[0], filters.get("agency")),
				as_list=1,
			)
			if total_employee[0][0]:
				label.append(parameter)
			datasets.append(total_employee[0][0])

	values = [value for value in datasets if value != 0]

	total_employee = frappe.db.count("Employee", {"status": "Active"})
	others = total_employee - sum(values)

	label.append(["Not Set"])
	values.append(others)

	chart = {"data": {"labels": label, "datasets": [{"name": "Employees", "values": values}]}}
	chart["type"] = "donut"
	return chart
