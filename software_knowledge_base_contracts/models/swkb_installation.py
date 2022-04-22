from odoo import fields, models


class SWKBInstallation(models.Model):
    _inherit = "software_knowledge_base.installation"

    contract_id = fields.Many2one(
        string="Contract",
        comodel_name="contract.contract",
        domain=[("recurring_invoices", "!=", False)],
        copy=False,
        related="contract_line_id.contract_id",
    )
    contract_line_id = fields.Many2one(
        string="Contract line",
        comodel_name="contract.line",
        copy=False,
    )
