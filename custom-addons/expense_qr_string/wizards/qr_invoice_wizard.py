from odoo import models, fields

class QRInvoiceWizard(models.TransientModel):
    _name = "qr.invoice.reader.wizard"
    _description = "QR Invoice Reader Wizard"

    qr_data = fields.Text("QR Code AT", required=True)
    expense_id = fields.Many2one("hr.expense")

    def action_process_qr(self):
        self.ensure_one()

        if self.expense_id:
            self.expense_id.qr_raw_string = self.qr_data

        return {"type": "ir.actions.act_window_close"}