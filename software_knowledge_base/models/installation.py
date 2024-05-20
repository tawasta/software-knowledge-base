from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Installation(models.Model):
    # 1. Private attributes
    _name = "software_knowledge_base.installation"
    _description = "Installation"
    _inherit = ["mail.thread"]
    _order = "name"

    _INSTALLATION_STATE_VALUES = [
        ("setup", "In setup"),
        ("ready", "In use"),
        ("terminated", "Terminated"),
    ]

    _INSTALLATION_TYPE_VALUES = [
        ("dev", "Dev"),
        ("test", "Test"),
        ("staging", "Staging"),
        ("production", "Production"),
    ]

    # 2. Fields declaration
    active = fields.Boolean(default=True)

    name = fields.Char(string="Name")

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id.id,
    )

    state = fields.Selection(
        selection=_INSTALLATION_STATE_VALUES,
        string="Status",
        help="What is the deployments status of the installation",
        default="setup",
    )

    type = fields.Selection(selection=_INSTALLATION_TYPE_VALUES, string="Type")

    additional_info = fields.Text(string="Additional info")

    platform_id = fields.Many2one(
        comodel_name="software_knowledge_base.platform", string="Platform"
    )

    server_id = fields.Many2one(
        comodel_name="software_knowledge_base.server", string="Server"
    )

    server_ip_address = fields.Char(
        string="Server IP-address", related="server_id.ip_address", store=True
    )

    port = fields.Integer(string="Port")

    db_server_id = fields.Many2one(
        comodel_name="software_knowledge_base.server", string="Database server"
    )

    db_server_ip_address = fields.Char(
        string="DB server IP-address", related="db_server_id.ip_address", store=True
    )

    disk_usage_min = fields.Float(
        string="Disk Usage Min (Gb)",
        help="The minimum amount of disk, this installation is expected to use",
    )
    disk_usage = fields.Float(
        string="Disk Usage (Gb)", help="Current disk usage in Gigabytes"
    )
    disk_usage_max = fields.Float(
        string="Disk Usage Max (Gb)",
        help="The maximum amount of disk, this installation is allowed to use",
    )
    disk_usage_percent = fields.Float(
        string="Disk usage %", compute="_compute_disk_usage_percent", store=True
    )

    url = fields.Char(string="URL")

    identifier = fields.Char(string="Identifier")

    user_accounts_active_min = fields.Integer(
        string="Min active users", help="Min active users"
    )
    user_accounts_active = fields.Integer(
        string="Active users", help="Current active users"
    )
    user_accounts_active_max = fields.Integer(
        string="Max active users", help="Max active users"
    )
    user_accounts_active_percent = fields.Float(
        string="Active users %",
        compute="_compute_user_accounts_active_percent",
        store=True,
    )

    user_accounts_total_min = fields.Integer(
        string="Min total users", help="Min total users"
    )
    user_accounts_total = fields.Integer(
        string="Total Users", help="Current total users"
    )
    user_accounts_total_max = fields.Integer(
        string="Max total users", help="Max total users"
    )
    user_accounts_total_percent = fields.Float(
        string="Total users %",
        compute="_compute_user_accounts_total_percent",
        store=True,
    )

    user_accounts_active_interval = fields.Integer(
        string="Active Interval", default="6"
    )
    user_accounts_active_type = fields.Selection(
        selection=[("days", "Days"), ("weeks", "Weeks"), ("months", "Months")],
        string="Interval Unit",
        default="months",
    )

    project_ids = fields.Many2many(
        comodel_name="project.project",
        relation="installation_project_rel",
        column1="installation_id",
        column2="project_id",
        string="Projects",
        help="Projects utilizing this installation.",
    )

    # Note the misnamed table module_partner_rel!
    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="module_partner_rel",
        column1="installation_id",
        column2="partner_id",
        string="Customers",
        help="Customers of this installation.",
    )

    module_ids = fields.Many2many(
        comodel_name="software_knowledge_base.module",
        relation="module_installation_rel",
        column1="installation_id",
        column2="module_id",
        string="Modules",
        help="Modules used by this installation.",
    )

    module_count = fields.Integer(
        string="Module count", compute="_compute_module_count"
    )

    external_component_ids = fields.Many2many(
        comodel_name="software_knowledge_base.external_component",
        relation="installation_ext_comp_rel",
        column1="installation_id",
        column2="ext_comp_id",
        string="External components",
        help=(
            "Libraries and other third party components used by this " "installation."
        ),
    )

    platform_image = fields.Image(string="Platform icon", related="platform_id.image")

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_module_count(self):
        for record in self:
            record.module_count = len(record.module_ids)

    @api.depends("disk_usage", "disk_usage_max")
    def _compute_disk_usage_percent(self):
        for record in self:
            if record.disk_usage_max == 0:
                record.disk_usage_percent = 0
            else:
                record.disk_usage_percent = (
                    record.disk_usage / record.disk_usage_max * 100
                )

    @api.depends("user_accounts_active", "user_accounts_active_max")
    def _compute_user_accounts_active_percent(self):
        for record in self:
            if record.user_accounts_active_max == 0:
                record.user_accounts_active_percent = 0
            else:
                record.user_accounts_active_percent = (
                    record.user_accounts_active / record.user_accounts_active_max * 100
                )

    @api.depends("user_accounts_total", "user_accounts_total_max")
    def _compute_user_accounts_total_percent(self):
        for record in self:
            if record.user_accounts_total_max == 0:
                record.user_accounts_total_percent = 0
            else:
                record.user_accounts_total_percent = (
                    record.user_accounts_total / record.user_accounts_total_max * 100
                )

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_view_modules(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "software_knowledge_base.modules_action"
        )
        action["domain"] = [("id", "in", self.module_ids.ids)]
        return action

    # 8. Business methods
    def update_info(self, **kwargs):
        """
        Helper for updating or creating installations
        url is used for matching existing installations
        kwargs can include fields to be saved as record values
        """
        url = kwargs.get("url")
        if not url:
            raise ValidationError(_("url is a mandatory field"))

        self.ensure_one()
        installation = self.search([("url", "=ilike", url)])

        if not installation:
            # Existing installation is not found - create a new one
            installation = self.create({"name": url, "url": url})

        # Update installation modules
        swkb_module = self.env["software_knowledge_base.module"]
        for module in kwargs.get("module_ids"):
            domain = [
                ("name", "=", module.get("name")),
                ("website", "=", module.get("website")),
            ]
            existing_module = swkb_module.search(domain, limit=1)

            if not existing_module:
                existing_module = swkb_module.create(module)

            if existing_module not in installation.module_ids:
                installation.module_ids = [(4, existing_module.id)]

        # Update installation users
        if kwargs.get("user_accounts_active"):
            installation.user_accounts_active = kwargs.get("user_accounts_active")
        if kwargs.get("user_accounts_total"):
            installation.user_accounts_total = kwargs.get("user_accounts_total")

        return installation.id
