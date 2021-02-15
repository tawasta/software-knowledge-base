from odoo import fields, models


class Module(models.Model):
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
    ]

    name = fields.Char(string="Name")

    summary = fields.Char(size=128, string="Summary")

    module_type = fields.Selection(
        selection=_MODULE_TYPE_VALUES,
        string="Module type",
        help="Where the module has been developed",
    )

    user_id = fields.Many2one(comodel_name="res.users", string="Responsible")

    features = fields.Text(string="Features")

    readme = fields.Text(string="Readme")

    installation_notes = fields.Text(string="Installation notes")

    issues = fields.Text(
        string="Issues",
        help=("Known bugs, limitations, incompatibilities with other " "modules etc."),
    )

    additional_info = fields.Text(
        string="Additional info", help="Additional information"
    )

    active = fields.Boolean(default=True)

    installation_ids = fields.Many2many(
        comodel_name="software_knowledge_base.installation",
        relation="module_installation_rel",
        column1="module_id",
        column2="installation_id",
        string="Installations",
        help="Where this module has been deployed.",
    )

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
