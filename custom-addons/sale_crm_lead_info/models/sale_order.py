from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    opportunity_id = fields.Many2one(
        'crm.lead',
        string="Oportunidade",
        index=True
    )
    
    crm_opportunity_id = fields.Char(
        string="",
        related='opportunity_id.oportunidade_id',
        store=True
    )

    crm_fieldservice_location = fields.Many2one(
        string="",
        related='opportunity_id.fsm_location_id',
        store=True
    )

    crm_fieldservice_location_name = fields.Char(
        string="Local FS (nome)",
        related='opportunity_id.fsm_location_id.name',
        store=True
    )


    opp_concat = fields.Char(
        string="Oportunidade + Código",
        compute="_compute_opp_concat",
        store=True  # gravar no DB
    )


    def action_open_opportunity(self):
        self.ensure_one()
        if not self.opportunity_id:
            return
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_mode': 'form',
            'res_id': self.opportunity_id.id,
            'target': 'new',  # abre em popup
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
        'views': [(False, 'form')],
        'res_id': location.id,
        'target': 'new',
        'context': dict(self.env.context or {}),
        }

    @api.depends('opportunity_id.oportunidade_id', 'opportunity_id.name')
    def _compute_opp_concat(self):
        for order in self:
            if order.opportunity_id:
                codigo = order.opportunity_id.oportunidade_id or ""
                nome = order.opportunity_id.name or ""
                order.opp_concat = f"{codigo} | {nome}" if codigo else nome
            else:
                order.opp_concat = ""