from odoo import models, fields

class QrInvoiceWizard(models.TransientModel):
    _inherit = "qr.invoice.wizard"

    crm_opportunity_id = fields.Many2one(
        "crm.lead",
        string="Oportunidade"
    )
