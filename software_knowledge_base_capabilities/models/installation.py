from odoo import api, fields, models


class Installation(models.Model):
    _inherit = "software_knowledge_base.installation"

    capability_ids = fields.Many2many(
        "swkb.capability",
        "skb_capability_installation_rel",
        "installation_id",
        "capability_id",
        string="Capabilities",
        help="Describes what type of installation or customer this is.",
        tracking=True,
    )

    capability_count = fields.Integer(
        compute="_compute_capability_count",
    )

    @api.depends("capability_ids")
    def _compute_capability_count(self):
        for rec in self:
            rec.capability_count = len(rec.capability_ids)

    def _get_target_module_ids(self):
        """Return a combined list of all module IDs from related capabilities."""
        all_ids = set()
        for rec in self:
            for cap in rec.capability_ids:
                all_ids |= cap._resolve_modules()
        return list(all_ids)

    def action_open_capability_apply_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "swkb.capability.apply.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_installation_id": self.id},
        }
