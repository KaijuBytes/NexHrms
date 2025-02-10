# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.model.document import Document


class ExpenseClaimType(Document):
	def validate(self):
		self.validate_accounts()
		self.validate_repeating_companies()

	def validate_repeating_companies(self):
		"""Error when Same Agency is entered multiple times in accounts"""
		accounts_list = []
		for entry in self.accounts:
			accounts_list.append(entry.agency)

		if len(accounts_list) != len(set(accounts_list)):
			frappe.throw(_("Same Agency is entered more than once"))

	def validate_accounts(self):
		for entry in self.accounts:
			"""Error when Agency of Ledger account doesn't match with Agency Selected"""
			if frappe.db.get_value("Account", entry.default_account, "agency") != entry.agency:
				frappe.throw(
					_("Account {0} does not match with Agency {1}").format(
						entry.default_account, entry.agency
					)
				)
