import logging
from odoo import api, fields, models



_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    # 1. Private attributes
    _inherit = "project.task"

    # 2. Fields declaration
    module_ids = fields.Many2many(
        comodel_name="software_knowledge_base.module",
        relation="module_task_rel",
        column1="task_id",
        column2="module_id",
        string="Modules",
        help="List here the modules that were affected by the work done in this task. "
        "If you created a new module, you can manually run the 'Software knowledge "
        "'base: export information' cron in the customer installation to get the "
        "module to immediately show up in Software Knowledge Base's list of modules.",
    )

    module_count = fields.Integer(
        string="Module count", compute="_compute_module_count"
    )

    installation_id = fields.Many2one(
        string="Installation",
        comodel_name="software_knowledge_base.installation",
        compute="_compute_installation_id",
        store=True,
        readonly=False,
    )
    installation_server_id = fields.Many2one(
        related="installation_id.server_id",
    )
    installation_db_server_id = fields.Many2one(
        related="installation_id.db_server_id",
    )
    installation_admin_url = fields.Char(
        related="installation_id.admin_url",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_module_count(self):
        for record in self:
            record.module_count = len(record.module_ids)

    @api.depends("partner_id")
    def _compute_installation_id(self):
        for record in self:
            installations = record.partner_id.installation_ids
            if not installations:
                installations = record.partner_id.commercial_partner_id.installation_ids

            prod_installations = installations.filtered(
                lambda i: i.type == "production"
            )

            if len(installations) == 1:
                record.installation_id = installations[0]
            elif len(prod_installations) == 1:
                record.installation_id = prod_installations[0]
            else:
                record.installation_id = False

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_view_modules(self):
        _logger.info("action reached")
        _logger.info(self.module_ids.ids)
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "software_knowledge_base.modules_action"
        )
        action["domain"] = [("id", "in", self.module_ids.ids)]
        return action

    # 8. Business methods
