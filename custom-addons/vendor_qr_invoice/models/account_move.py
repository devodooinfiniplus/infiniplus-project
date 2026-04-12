from odoo import models

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_open_qr_scanner(self):
        return {
            "type": "ir.actions.client",
            "tag": "qr_scanner_action",
        }
