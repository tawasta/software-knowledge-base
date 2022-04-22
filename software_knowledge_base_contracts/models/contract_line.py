from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    installation_ids = fields.One2many(
        string="Installation",
        comodel_name="software_knowledge_base.installation",
        inverse_name="contract_line_id",
        copy=False,
    )
