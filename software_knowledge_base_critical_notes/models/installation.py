from odoo import api, fields, models


class SWKBInstallation(models.Model):
    _inherit = "software_knowledge_base.installation"

    note_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation.note",
        inverse_name="installation_id",
        string="Notes",
    )
    note_count = fields.Integer(compute="_compute_note_count")
    critical_alert_enabled = fields.Boolean(
        string="Show critical note alerts on tasks",
        default=True,
        help="When enabled, this installation's critical notes are shown "
        "as a warning on every linked task or ticket. Turn off to silence "
        "the alert for this installation without deleting the notes.",
    )

    @api.depends("note_ids")
    def _compute_note_count(self):
        for record in self:
            record.note_count = len(record.note_ids)

    def action_open_notes(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "software_knowledge_base_critical_notes.installation_note_action"
        )
        action["domain"] = [("installation_id", "=", self.id)]
        action["context"] = {"default_installation_id": self.id}
        return action
