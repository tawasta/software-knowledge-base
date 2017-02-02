# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class project_task(osv.Model):
    
    _inherit = 'project.task'
                
    _columns = {
        'module_ids': fields.many2many('software_knowledge_base.module', 'module_task_rel',  'task_id', 'module_id',
                                        string='Modules', help='Related modules'),
    }
