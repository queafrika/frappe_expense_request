# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bantoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document
from erpnext.accounts.doctype.journal_entry.journal_entry import make_reverse_journal_entry


class ExpenseEntry(Document):
    
    def on_cancel(self):  
        
        if frappe.db.exists({'doctype': 'Journal Entry', 'bill_no': self.name}):
            
            jes = frappe.get_all("Journal Entry", filters=[["bill_no", "=", self.name]])

            for je in jes:
                rje = make_reverse_journal_entry(je.name)
                rje.posting_date = frappe.utils.nowdate()
                rje.submit()

    def before_save(self):
        # autofill remarks with expense type if empty
        if not self.remarks:
            self.remarks = ""
        
        for entry in self.expenses:
            self.remarks += entry.expense_account + ": " + str(entry.amount) + "\n"
        
        self.save()
            