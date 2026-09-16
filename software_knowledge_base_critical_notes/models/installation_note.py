from odoo import _, api, fields, models


class SWKBInstallationNote(models.Model):
    _name = "software_knowledge_base.installation.note"
    _description = "Installation Note"
    _order = "is_critical desc, sequence, id"

    installation_id = fields.Many2one(
        comodel_name="software_knowledge_base.installation",
        required=True,
        ondelete="cascade",
        index=True,
    )
    name = fields.Char(string="Title", required=True)
    description = fields.Html(sanitize=True)
    is_critical = fields.Boolean(
        string="Critical",
        help="Critical notes are shown as a warning on every task or "
        "ticket linked to this installation. Non-critical notes are only "
        "visible on the installation record itself.",
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        notes = super().create(vals_list)
        for note in notes.filtered("is_critical"):
            note.installation_id.message_post(
                body=_("Critical note added: %s", note.name)
            )
        return notes

    def write(self, vals):
        res = super().write(vals)
        if "is_critical" in vals:
            for note in self:
                message = (
                    _("Marked as critical: %s", note.name)
                    if note.is_critical
                    else _("No longer marked as critical: %s", note.name)
                )
                note.installation_id.message_post(body=message)
        elif set(vals) & {"name", "description"}:
            for note in self.filtered("is_critical"):
                note.installation_id.message_post(
                    body=_("Critical note updated: %s", note.name)
                )
        return res
