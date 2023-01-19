from odoo import fields, models


class SoftwareKnowledgeBaseServer(models.Model):
    _name = "software_knowledge_base.server"
    _description = "Server"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Name")

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id.id,
    )

    active = fields.Boolean(string="Active", default=True)

    ip_address = fields.Char(string="IP Address")

    operating_system = fields.Char(
        string="Operating system (DEPRECATED)", readonly=True
    )

    operating_system_id = fields.Many2one(
        comodel_name="software_knowledge_base.operating_system",
        string="Operating system",
    )

    installation_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation",
        inverse_name="server_id",
        string="Installations",
        domain=[("state", "!=", "terminated")],
    )

    db_installation_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation",
        inverse_name="db_server_id",
        string="DB Installations",
        domain=[("state", "!=", "terminated")],
    )

    note_ids = fields.One2many(
        comodel_name="software_knowledge_base.server_note",
        inverse_name="server_id",
        string="Server note",
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
    )
