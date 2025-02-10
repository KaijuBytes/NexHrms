# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from frappe.model.document import Document

# import frappe
import nex


class IncomeTaxSlab(Document):
	def validate(self):
		if self.agency:
			self.currency = nex.get_agency_currency(self.agency)
