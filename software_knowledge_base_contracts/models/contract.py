from odoo import fields, models


class Contract(models.Model):
    _inherit = "contract.contract"

    installation_ids = fields.Many2many(
        string="Installations",
        comodel_name="software_knowledge_base.installation",
        copy=False,
        compute="_compute_installation_ids",
    )

    installation_count = fields.Integer(
        string="Installation count", compute="_compute_installation_count"
    )

    def _compute_installation_ids(self):
        for record in self:
            record.installation_ids = record.contract_line_ids.mapped(
                "installation_ids"
            )

    def _compute_installation_count(self):
        for record in self:
            record.installation_count = len(record.installation_ids)
