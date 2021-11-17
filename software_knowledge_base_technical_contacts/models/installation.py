##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class Installation(models.Model):
    # 1. Private attributes
    _inherit = "software_knowledge_base.installation"

    # 2. Fields declaration
    technical_contact_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="installation_techcontact_rel",
        column1="instalation_id",
        column2="partner_id",
        string="Technical contacts",
        help="Technical contacts for this installation",
        domain=[("is_company", "=", False)],
    )

    technical_contact_emails = fields.Char(
        string="Technical contact emails", compute="_compute_technical_contact_emails"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_technical_contact_emails(self):
        # Technical contacts in a copy-ready string
        for record in self:
            emails = filter(None, record.technical_contact_ids.mapped("email"))
            record.technical_contact_emails = ", ".join(emails)

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
