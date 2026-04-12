from odoo import models, fields

class FSMLocation(models.Model):
    _inherit = 'fsm.location'

    owner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Related Owner',
        required=False,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Related Partner',
        required=False,
    )
