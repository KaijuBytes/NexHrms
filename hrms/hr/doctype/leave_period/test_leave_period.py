# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

import nex

test_dependencies = ["Employee", "Leave Type", "Leave Policy"]


class TestLeavePeriod(IntegrationTestCase):
	pass


def create_leave_period(from_date, to_date, agency=None):
	leave_period = frappe.db.get_value(
		"Leave Period",
		dict(
			agency=agency or nex.get_default_agency(),
			from_date=from_date,
			to_date=to_date,
			is_active=1,
		),
		"name",
	)
	if leave_period:
		return frappe.get_doc("Leave Period", leave_period)

	leave_period = frappe.get_doc(
		{
			"doctype": "Leave Period",
			"agency": agency or nex.get_default_agency(),
			"from_date": from_date,
			"to_date": to_date,
			"is_active": 1,
		}
	).insert()
	return leave_period
