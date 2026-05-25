from odoo import api, fields, models


class SoftwareKnowledgeBaseServer(models.Model):
    _name = "software_knowledge_base.server"
    _description = "Server"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char()

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id.id,
    )

    active = fields.Boolean(default=True)

    ip_address = fields.Char(string="IP Address")

    operating_system = fields.Char(
        string="Operating system (DEPRECATED)", readonly=True
    )

    # Please maintain an alphabetical order here
    server_type = fields.Selection(
        [
            ("application", "Application server"),
            ("database", "Database server"),
            ("dhcp", "DHCP server"),
            ("dns", "DNS server"),
            ("file", "File server"),
            ("mail", "Mail server"),
            ("other", "Other server"),
            ("print", "Print server"),
            ("proxy", "Proxy server"),
            ("web", "Web server"),
        ],
    )

    operating_system_id = fields.Many2one(
        comodel_name="software_knowledge_base.operating_system",
        string="Operating system",
        tracking=True,
    )

    installation_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation",
        inverse_name="server_id",
        string="Installations",
        domain=[("state", "!=", "terminated")],
    )

    installation_count = fields.Integer(
        string="Installation count", compute="_compute_installation_count", store=False
    )

    db_connections_limit = fields.Integer(
        "DB Connections limit",
    )
    db_connections_used = fields.Integer(
        "DB Connections used", compute="_compute_db_connections_used"
    )
    db_installation_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation",
        inverse_name="db_server_id",
        string="DB Installations",
        domain=[("state", "!=", "terminated")],
    )
    db_connections_percent = fields.Float(
        "DB Connections %",
        help="Percentage of used DB connections",
        compute="_compute_db_connections_percent",
    )

    note_ids = fields.One2many(
        comodel_name="software_knowledge_base.server_note",
        inverse_name="server_id",
        string="Server note",
    )
    note_count = fields.Integer(
        string="Notes", compute="_compute_note_count", store=False
    )

    cpu_cores = fields.Integer("CPU Cores")
    ram = fields.Integer("RAM (Gb)")

    disk_size = fields.Float("Disk size (Gb)")
    disk_used = fields.Float(
        "Used disk (Gb)",
        compute="_compute_disk_usage",
    )
    disk_available = fields.Float(
        "Available disk (Gb)",
        compute="_compute_disk_usage",
    )
    disk_usage_percent = fields.Float(
        string="Disk usage %", compute="_compute_disk_usage"
    )

    specification = fields.Text(string="Technical specification")

    additional_info = fields.Text(string="Additional info")

    supplier_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        help="The supplier of this server",
        domain=[("is_company", "=", True), ("supplier_rank", ">", 0)],
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        help="Appointed responsible person for this server",
        default=lambda self: self.env.user,
        tracking=True,
    )

    module_count = fields.Integer(
        string="Module count", compute="_compute_module_count"
    )

    @api.depends("installation_ids")
    def _compute_installation_count(self):
        for server in self:
            server.installation_count = len(server.installation_ids)

    @api.depends("note_ids")
    def _compute_note_count(self):
        for server in self:
            server.note_count = len(server.note_ids)

    @api.depends("disk_size", "disk_used")
    def _compute_disk_usage(self):
        for record in self:
            record.disk_used = sum(record.installation_ids.mapped("disk_usage"))
            record.disk_available = record.disk_size - record.disk_used

            disk_usage_percent = 0
            if record.disk_size and record.disk_used > 0:
                disk_usage_percent = record.disk_used / record.disk_size * 100

            record.disk_usage_percent = disk_usage_percent

    @api.depends("db_installation_ids")
    def _compute_db_connections_used(self):
        for record in self:
            record.db_connections_used = sum(
                record.db_installation_ids.mapped("db_connections_used")
            )

    @api.depends("db_connections_limit", "db_connections_used")
    def _compute_db_connections_percent(self):
        for record in self:
            if record.db_connections_limit:
                record.db_connections_percent = (
                    record.db_connections_used / record.db_connections_limit * 100
                )
            else:
                record.db_connections_percent = 0

    def _compute_module_count(self):
        for record in self:
            record.module_count = len(record.mapped("installation_ids.module_ids"))

    def action_open_installations(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "software_knowledge_base.installation",
            "view_mode": "tree,form",
            "domain": [("server_id", "in", self.ids)],
            "name": "Installations",
        }

    def action_open_modules(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "software_knowledge_base.modules_action"
        )
        module_ids = self.mapped("installation_ids.module_ids").ids

        action["domain"] = [("id", "in", module_ids)]
        return action

    def action_open_notes(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "software_knowledge_base.server_note",
            "view_mode": "tree,form",
            "domain": [("server_id", "in", self.ids)],
            "name": "Notes",
        }
