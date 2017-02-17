# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_partner(osv.Model):
    
    _inherit = 'res.partner'
                
    _columns = {
        #'installation_ids': fields.one2many('software_knowledge_base.installation', 'partner_id', 'Installations'),

        # Note the misnamed table module_partner_rel!
        'installation_ids':     fields.many2many('software_knowledge_base.installation', 'module_partner_rel', 'partner_id', 'installation_id',
                                                 string='Installations'),        
    }
