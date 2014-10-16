# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class project_project(osv.Model):
    
    _inherit = 'project.project'
                
    _columns = {
        'installation_ids': fields.one2many('software_knowledge_base.installation', 'project_id', 'Installations'),
    }
