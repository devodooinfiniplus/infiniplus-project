from odoo import models, fields
from datetime import datetime

class QRInvoiceWizard(models.TransientModel):
    _name = "qr.invoice.wizard"
    _description = "QR Invoice Wizard"

    qr_data = fields.Text("QR Code AT", required=True)

    def _parse_at_qr(self):
        data = {}
        for part in self.qr_data.split("*"):
            if ":" in part:
                k, v = part.split(":", 1)
                data[k] = v
        return data

    def action_process_qr(self):
        self.ensure_one()
        data = self._parse_at_qr()

        nif = data.get("A")
        name = data.get("B") or f"Fornecedor {nif}"

        partner = self.env["res.partner"].search(
            [("vat", "=", f"PT{nif}")], limit=1
        )
        if not partner:
            partner = self.env["res.partner"].create({
                "name": name,
                "vat": f"PT{nif}",
                "supplier_rank": 1,
            })

        date = datetime.strptime(data.get("F"), "%Y%m%d").date()
        total = float(data.get("O", "0").replace(",", "."))

        move = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": partner.id,
            "invoice_date": date,
            "invoice_line_ids": [(0, 0, {
                "name": "Fatura via QR AT",
                "quantity": 1,
                "price_unit": total,
            })],
        })

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
        }
