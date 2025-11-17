from odoo import api, fields, models


class Installation(models.Model):
    _inherit = "software_knowledge_base.installation"

    capability_line_ids = fields.One2many(
        "swkb.capability.installation.line",
        "installation_id",
        string="Capabilities",
        help="Capabilities linked to this installation with status per row.",
        tracking=True,
    )

    capability_count = fields.Integer(
        compute="_compute_capability_count",
        store=False,
    )

    @api.depends("capability_line_ids.capability_id")
    def _compute_capability_count(self):
        for rec in self:
            caps = rec.capability_line_ids.mapped("capability_id").ids
            rec.capability_count = len(set(caps))

    def _get_target_module_ids(self):
        """Return a combined list of all module IDs from related capabilities."""
        all_ids = set()
        for rec in self:
            for line in rec.capability_line_ids:
                if line.capability_id:
                    all_ids |= line.capability_id._resolve_modules()
        return list(all_ids)
