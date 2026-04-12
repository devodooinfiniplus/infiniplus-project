from odoo import models, fields, api
    

class AccountMove(models.Model):
    _inherit = 'account.move'

    crm_opportunity_id = fields.Char(
        string="",
        related='sale_order_id.opportunity_id.oportunidade_id',
        store=True
    )

    sale_order_id = fields.Many2one(
        'sale.order',
        compute='_compute_sale_order_id',
        store=True,
        string=''
    )

    crm_fieldservice_location = fields.Many2one(
        string="",
        related='sale_order_id.opportunity_id.fsm_location_id',
        store=True
    )

    sale_lead_oppotunity_display = fields.Char(
        compute='_compute_sale_lead_oppotunity_display',
        store=True,
        string=''
    )

    crm_fieldservice_location_name = fields.Char(
        related='sale_order_id.opportunity_id.fsm_location_id.name',
        store=True,
        string='Local FS (nome)'
    )

    def action_open_opportunity(self):
        self.ensure_one()
        if not self.crm_opportunity_id:
            return
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_mode': 'form',
            'res_id': self.sale_order_id.opportunity_id.id,
            'target': 'new',
        }

    def action_open_fieldservice_location(self):
        self.ensure_one()
        location = self.crm_fieldservice_location
        if not location:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Local Field Service',
            'res_model': 'fsm.location',
            'view_mode': 'form',
            'res_id': location.id,
            'target': 'new',
        }

    @api.depends('invoice_origin')
    def _compute_sale_order_id(self):
        for record in self:
            record.sale_order_id = self.env['sale.order'].search([
                ('name', '=', record.invoice_origin)
            ], limit=1)

    @api.depends('crm_opportunity_id', 'sale_order_id.name')
    def _compute_sale_lead_oppotunity_display(self):
        for record in self:
            order_name = record.sale_order_id.opportunity_id.name or ''
            record.sale_lead_oppotunity_display = f"{record.crm_opportunity_id} | {order_name}" if record.crm_opportunity_id else order_name
