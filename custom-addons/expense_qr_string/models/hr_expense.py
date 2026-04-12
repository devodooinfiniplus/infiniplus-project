from odoo import models, fields, api
from odoo.tools import date_utils
from datetime import datetime

class HrExpense(models.Model):
    _inherit = "hr.expense"

    qr_raw_string = fields.Char(
        string="Código AT capturado",
        copy=False
    )

    def action_open_qr_scanner(self):
        self.ensure_one()
        return {
        "type": "ir.actions.client",
        "tag": "expense_qr_scanner",
        "target": "new", 
        "params": {
            "expense_id": self.id
        }
    }


    def _parse_qr_at(self):
        self.ensure_one()

        if not self.qr_raw_string:
            return {}

        data = {}
        parts = self.qr_raw_string.split("*")

        for part in parts:
            if ":" in part:
                key, value = part.split(":", 1)
                data[key] = value

        return data

    def write(self, vals):
        res = super().write(vals)

        if "qr_raw_string" in vals:
            for expense in self:
                if expense.qr_raw_string:
                    qr_data = expense._parse_qr_at()
                    total = qr_data.get("O")

                if total:
                    try:
                        total_value = float(total)

                        expense.total_amount = total_value
                        expense.total_amount_currency = total_value

                    except ValueError:
                        pass

        return res