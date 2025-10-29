# Copyright (c) 2025,   and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomSalesOrder(Document):
    
	def validate(self):
		if(self.delivery_date < self.delivery_date):
			frappe.msgprint("Expected Delivery Date should be after Sales Order Date.")
   
	