from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    show_installation_critical_notice = fields.Boolean(
        compute="_compute_installation_critical_notice",
        store=True,
    )
    installation_critical_note_count = fields.Integer(
        compute="_compute_installation_critical_notice",
        store=True,
    )
    installation_critical_notice_html = fields.Html(
        compute="_compute_installation_critical_notice",
        sanitize=False,
    )

    @api.depends(
        "installation_id.critical_alert_enabled",
        "installation_id.note_ids.active",
        "installation_id.note_ids.is_critical",
        "installation_id.note_ids.name",
        "installation_id.note_ids.description",
    )
    def _compute_installation_critical_notice(self):
        for task in self:
            critical_notes = task.installation_id.note_ids.filtered("is_critical")
            task.show_installation_critical_notice = bool(
                task.installation_id.critical_alert_enabled and critical_notes
            )
            task.installation_critical_note_count = len(critical_notes)
            task.installation_critical_notice_html = (
                self.env["ir.qweb"]._render(
                    "software_knowledge_base_critical_notes.critical_notes_list",
                    {"notes": critical_notes},
                )
                if critical_notes
                else False
            )
