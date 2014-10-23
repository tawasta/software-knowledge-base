# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class project_project(osv.Model):
    
    _inherit = 'project.project'
                
    _columns = {
        #'installation_ids': fields.one2many('software_knowledge_base.installation', 'project_id', 'Installations'),
        'installation_ids':  fields.many2many('software_knowledge_base.installation', 'installation_project_rel', 'project_id', 'installation_id',
                                                 string='Installations', help='Installations related to this project.'),        
    }
