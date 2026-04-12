from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        move = super().create(vals)

        print("DEBUG ACCOUNT MOVE CREATE")
        # Só mexer em faturas de fornecedor criadas por despesas
        if move.move_type == "in_invoice" and move.ref:
            
            # Procurar despesa com QR associado
            expense = self.env["hr.expense"].search([
                ("name", "=", move.ref),
                ("qr_raw_string", "!=", False)
            ], limit=1)

            if expense:
                qr_data = expense._parse_qr_at()
                update_vals = {}

                # FORNECEDOR
                nif = qr_data.get("A")
                if nif:
                    partner = self.env["res.partner"].search(
                        [("vat", "=", nif)],
                        limit=1
                    )

                    if not partner:
                        partner = self.env["res.partner"].create({
                            "name": f"Fornecedor {nif}",
                            "vat": nif,
                            "company_type": "company",
                        })

                    update_vals["partner_id"] = partner.id

                # DATA
                if qr_data.get("F"):
                    raw = qr_data["F"]
                    invoice_date = fields.Date.from_string(
                        f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"
                    )

                    update_vals["invoice_date"] = invoice_date
                    update_vals["date"] = invoice_date

                if update_vals:
                    move.write(update_vals)

        return move