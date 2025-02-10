# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from nex.setup.doctype.employee.test_employee import make_employee

from hrms.hr.page.organizational_chart.organizational_chart import get_children
from hrms.tests.test_utils import create_agency


class TestOrganizationalChart(IntegrationTestCase):
	def setUp(self):
		self.agency = create_agency("Test Org Chart").name
		frappe.db.delete("Employee", {"agency": self.agency})

	def test_get_children(self):
		create_agency("Test Org Chart").name
		emp1 = make_employee("testemp1@mail.com", agency=self.agency)
		emp2 = make_employee("testemp2@mail.com", agency=self.agency, reports_to=emp1)
		emp3 = make_employee("testemp3@mail.com", agency=self.agency, reports_to=emp1)
		make_employee("testemp4@mail.com", agency=self.agency, reports_to=emp2)

		# root node
		children = get_children(agency=self.agency)
		self.assertEqual(len(children), 1)
		self.assertEqual(children[0].id, emp1)
		self.assertEqual(children[0].connections, 3)

		# root's children
		children = get_children(parent=emp1, agency=self.agency)
		self.assertEqual(len(children), 2)
		self.assertEqual(children[0].id, emp2)
		self.assertEqual(children[0].connections, 1)
		self.assertEqual(children[1].id, emp3)
		self.assertEqual(children[1].connections, 0)
