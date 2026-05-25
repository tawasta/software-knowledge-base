from odoo import api, fields, models


class Module(models.Model):
    # 1. Private attributes
    _name = "software_knowledge_base.module"
    _description = "Module"
    _inherit = ["mail.thread"]
    _order = "name"

    _MODULE_TYPE_VALUES = [
        ("core", "Core"),
        ("community", "Community"),
        ("community_commercial", "Community (commercial)"),
        ("inhouse", "In-house"),
        ("inhouse_commercial", "In-house (commercial)"),
        ("third_party", "Third party"),
    ]

    # 2. Fields declaration
    name = fields.Char()
    description = fields.Char()
    author = fields.Char()
    website = fields.Char()
    summary = fields.Char(size=128)
    color = fields.Integer(compute="_compute_color", store=True)

    module_type = fields.Selection(
        selection=_MODULE_TYPE_VALUES,
        help="Where the module has been developed",
    )

    user_id = fields.Many2one(comodel_name="res.users", string="Responsible")

    features = fields.Text()

    readme = fields.Text()

    installation_notes = fields.Text()

    issues = fields.Text(
        help=("Known bugs, limitations, incompatibilities with other " "modules etc."),
    )

    additional_info = fields.Text(help="Additional information")

    active = fields.Boolean(default=True)

    installation_ids = fields.Many2many(
        comodel_name="software_knowledge_base.installation",
        relation="module_installation_rel",
        column1="module_id",
        column2="installation_id",
        string="Installations",
        help="Where this module has been deployed.",
    )

    installation_count = fields.Integer(compute="_compute_installation_count")

    task_ids = fields.Many2many(
        comodel_name="project.task",
        relation="module_task_rel",
        column1="module_id",
        column2="task_id",
        string="Tasks",
        help="Related project management tasks",
    )

    platform_ids = fields.Many2many(
        comodel_name="software_knowledge_base.platform",
        relation="module_platform_rel",
        column1="module_id",
        column2="platform_id",
        string="Platforms",
        help="Supported platforms",
    )

    project_tag_ids = fields.Many2many(
        comodel_name="project.tags",
        relation="module_project_tag_rel",
        column1="module_id",
        column2="tag_id",
        string="Project tags",
        help="Project tags related to this module. \n"
        "The tags will be automatically added to task, \n"
        "when linking them to the module.",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends("website")
    def _compute_color(self):
        """
        Give the module an arbitrary color code between 1-11 based on the
        repository URL, i.e. all modules from the same repo will be the
        same color.
        """
        for record in self:
            if not record.website:
                record.color = 1
            else:
                # Trim trailing slash
                website = (
                    record.website.endswith("/")
                    and record.website[:-1]
                    or record.website
                )
                record.color = sum(ord(char) for char in website) % 11 + 1

    def _compute_installation_count(self):
        for record in self:
            record.installation_count = len(record.installation_ids)

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_open_installations(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "software_knowledge_base.installations_action"
        )
        action["domain"] = [("id", "in", self.installation_ids.ids)]
        return action

    # 8. Business methods
