# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBInstallation(models.Model):
    # 1. Private attributes
    _inherit = "software_knowledge_base.installation"

    # 2. Fields declaration
    classification_ids = fields.Many2many(
        comodel_name="software_knowledge_base.installation.classification",
        relation="installation_classification_rel",
        string="Classifications",
        help="Classifications for this installation",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
