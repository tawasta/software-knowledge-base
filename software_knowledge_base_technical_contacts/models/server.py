from odoo import _, api, fields, models


class Server(models.Model):

    _inherit = "software_knowledge_base.server"

    technical_contact_ids = fields.Many2many(
        comodel_name="res.partner",
        string=_("Technical contact"),
        compute="compute_technical_contact_ids",
    )

    technical_contact_emails = fields.Char(
        string="Technical contact emails", compute="compute_technical_contact_emails",
    )

    @api.multi
    def compute_technical_contact_ids(self):
        ResPartner = self.env["res.partner"]

        for record in self:
            technical_contact_ids = []

            for installation in record.installation_ids:
                technical_contact_ids += installation.technical_contact_ids.ids

            record.technical_contact_ids = ResPartner.browse(technical_contact_ids)

    @api.multi
    def compute_technical_contact_emails(self):
        # Technical contacts in copy-ready string
        for record in self:
            record.technical_contact_emails = ", ".join(
                [contact.email for contact in record.technical_contact_ids]
            )
