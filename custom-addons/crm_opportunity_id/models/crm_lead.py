from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = "crm.lead"


    def action_open_qr_scanner(self):
        return {
            "type": "ir.actions.client",
            "tag": "qr_scanner_action",
            "context": {
                "default_crm_opportunity_id": self.id,
        },
    }



    currency_id = fields.Many2one(
    'res.currency',
    string='Moeda',
    default=lambda self: self.env.company.currency_id
    )


    oportunidade_id = fields.Char(
        string="ID Oportunidade",
        readonly=True,
        copy=True,
        index=True,
    )

    @api.model
    def create(self, vals):
        if not vals.get("oportunidade_id"):
            vals["oportunidade_id"] = self.env["ir.sequence"].next_by_code("crm.lead.opportunity") or "/"
        return super().create(vals)

    #PERCENTAGEM DE EXECUCAO
    execution_percentage = fields.Float(
           string='Execução (%)',
        compute="_compute_execution_percentage",
        store=True,   # grava na BD, útil para pesquisa/filtrar
        readonly=True
    )

    @api.depends('stage_id')
    def _compute_execution_percentage(self):
        """
        Exemplo simples: percentagem = posição da etapa no pipeline.
        Adapta a lógica às tuas regras (tarefas concluídas, valor, etc.).
        """
        for lead in self:
            stages = self.env['crm.stage'].search([('team_id', '=', lead.team_id.id)], order='sequence')
            if stages:
                idx = stages.ids.index(lead.stage_id.id) if lead.stage_id.id in stages.ids else 0
                lead.execution_percentage = round((idx + 1) / len(stages) * 100, 2)
            else:
                lead.execution_percentage = 0.0


    #PERCENTAGEM DE FATURACAO
     # Cria a relação inversa para todos os pedidos ligados a este lead
    order_ids = fields.One2many(
        'sale.order',
        'opportunity_id',
        string='Pedidos de Venda'
    )

    # Percentagem de faturação
    billing_percentage = fields.Float(
        string='Faturação (%)',
        compute='_compute_billing_percentage',
        store=True,
        help='Percentagem faturada face ao valor previsto'
    )

    @api.depends('order_ids.invoice_ids.amount_total', 'expected_revenue')
    def _compute_billing_percentage(self):
        for lead in self:
            total_invoiced = sum(
                inv.amount_total
                for inv in lead.mapped('order_ids.invoice_ids')
                if inv.state == 'posted'
            )
            lead.billing_percentage = (
                (total_invoiced / lead.expected_revenue) * 100
                if lead.expected_revenue else 0.0
            )

    amount_received = fields.Monetary(string="Valor Recebido",
    currency_field="currency_id")

    receipt_percent = fields.Float(
    string="Recebimento (%)",
    compute="_compute_receipt_percent",
    store=True
    )


    @api.depends('amount_received', 'expected_revenue')
    def _compute_receipt_percent(self):
        for lead in self:
            if lead.expected_revenue > 0:
                lead.receipt_percent = (lead.amount_received / lead.expected_revenue) * 100
            else:
                lead.receipt_percent = 0.0