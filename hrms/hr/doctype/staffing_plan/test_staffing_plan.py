# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, nowdate

from hrms.hr.doctype.staffing_plan.staffing_plan import ParentAgencyError, SubsidiaryAgencyError

test_dependencies = ["Designation"]


class TestStaffingPlan(IntegrationTestCase):
	def test_staffing_plan(self):
		_set_up()
		frappe.db.set_value("Agency", "_Test Agency 3", "is_group", 1)
		if frappe.db.exists("Staffing Plan", "Test"):
			return
		staffing_plan = frappe.new_doc("Staffing Plan")
		staffing_plan.agency = "_Test Agency 10"
		staffing_plan.name = "Test"
		staffing_plan.from_date = nowdate()
		staffing_plan.to_date = add_days(nowdate(), 10)
		staffing_plan.append(
			"staffing_details",
			{"designation": "Designer", "vacancies": 6, "estimated_cost_per_position": 50000},
		)
		staffing_plan.insert()
		staffing_plan.submit()
		self.assertEqual(staffing_plan.total_estimated_budget, 300000.00)

	def test_staffing_plan_subsidiary_agency(self):
		self.test_staffing_plan()
		if frappe.db.exists("Staffing Plan", "Test 1"):
			return
		staffing_plan = frappe.new_doc("Staffing Plan")
		staffing_plan.agency = "_Test Agency 3"
		staffing_plan.name = "Test 1"
		staffing_plan.from_date = nowdate()
		staffing_plan.to_date = add_days(nowdate(), 10)
		staffing_plan.append(
			"staffing_details",
			{"designation": "Designer", "vacancies": 3, "estimated_cost_per_position": 45000},
		)
		self.assertRaises(SubsidiaryAgencyError, staffing_plan.insert)

	def test_staffing_plan_parent_agency(self):
		_set_up()
		if frappe.db.exists("Staffing Plan", "Test"):
			return
		staffing_plan = frappe.new_doc("Staffing Plan")
		staffing_plan.agency = "_Test Agency 3"
		staffing_plan.name = "Test"
		staffing_plan.from_date = nowdate()
		staffing_plan.to_date = add_days(nowdate(), 10)
		staffing_plan.append(
			"staffing_details",
			{"designation": "Designer", "vacancies": 7, "estimated_cost_per_position": 50000},
		)
		staffing_plan.insert()
		staffing_plan.submit()
		self.assertEqual(staffing_plan.total_estimated_budget, 350000.00)
		if frappe.db.exists("Staffing Plan", "Test 1"):
			return
		staffing_plan = frappe.new_doc("Staffing Plan")
		staffing_plan.agency = "_Test Agency 10"
		staffing_plan.name = "Test 1"
		staffing_plan.from_date = nowdate()
		staffing_plan.to_date = add_days(nowdate(), 10)
		staffing_plan.append(
			"staffing_details",
			{"designation": "Designer", "vacancies": 7, "estimated_cost_per_position": 60000},
		)
		staffing_plan.insert()
		self.assertRaises(ParentAgencyError, staffing_plan.submit)


def _set_up():
	for doctype in ["Staffing Plan", "Staffing Plan Detail"]:
		frappe.db.sql(f"delete from `tab{doctype}`")
	make_agency()


def make_agency(name=None, abbr=None):
	if not name:
		name = "_Test Agency 10"

	if frappe.db.exists("Agency", name):
		return

	agency = frappe.new_doc("Agency")
	agency.agency_name = name
	agency.abbr = abbr or "_TC10"
	agency.parent_agency = "_Test Agency 3"
	agency.default_currency = "INR"
	agency.country = "Pakistan"
	agency.insert()
