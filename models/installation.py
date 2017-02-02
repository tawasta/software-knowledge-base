# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)


class installation(osv.Model):
    
    _name = 'software_knowledge_base.installation'
    _description = 'Installation'  
    _inherit = ['mail.thread']    
    _order = 'name'
    
    _INSTALLATION_STATE_VALUES = [('setup','In setup'),
                                  ('ready','In use'),
                                  ('terminated','Terminated')]
    

    def _copy_inst_data_to_m2m_field(self, cr, uid, ids=None, context=None):
        ''' In 2/2015 a change was added that enables an installation to be linked to many
        partners. This code is run on module install/update, it copies the data in the m2o
        field to the new m2m field, thus preserving the relationships that were done prior to the
        update. '''

        
        _logger.info('Starting to update installations data format')
        installations_with_unmoved_data = self.search(cr, uid, args=[('data_copied_to_m2m','=',False)], context=context)
        
        _logger.info('Found %i installations that use the old many2one relation. Starting to update...' % len(installations_with_unmoved_data))        
        for inst in self.browse(cr, uid, installations_with_unmoved_data):
            inst_vals = {
                'data_copied_to_m2m': True            
            }
            
            if inst.partner_id:
                _logger.info('Installation %s had a matching partner %s. Add a reference to the m2m field...' % (inst.name, inst.partner_id.name) )
                inst_vals['partner_ids'] = [(4, inst.partner_id.id)]
            
            self.write(cr, uid, [inst.id], inst_vals, context=context)

                    
        return True
        
    def copy(self, cr, uid, id, default=None, context=None):
        ''' Set default data_copied_to_m2m to allow copying installations without being admin '''
        default['data_copied_to_m2m'] = True
        
        return super(installation, self).copy(cr, uid, id, default, context=context)
        
    _columns = {
        'name':             fields.char('Name'),
        'company_id': fields.many2one('res.company', 'Company'),
        
        'state':            fields.selection(_INSTALLATION_STATE_VALUES, 'Status', help='Where the module has been developed'),
        'additional_info':  fields.text('Additional info'),
        
        'platform_id':      fields.many2one('software_knowledge_base.platform', string='Platform'),
        'server_id':        fields.many2one('software_knowledge_base.server', string='Server'),
        'port':             fields.integer('Port'),
        'db_server_id':     fields.many2one('software_knowledge_base.server', string='Database server'),
        'disk_usage':       fields.float('Disk Usage (MB)'),
        'url':              fields.char('URL'),
        'identifier':       fields.char('Identifier'),
        
        'project_ids':     fields.many2many('project.project', 'installation_project_rel', 'installation_id', 'project_id',
                                                 string='Projects', help='Projects utilizing this installation.'),
                        
        'partner_id':       fields.many2one('res.partner', string='Customer'), # Legacy field from where there was just 1 partner linked to inst.

        # Note the misnamed table module_partner_rel!
        'partner_ids':     fields.many2many('res.partner', 'module_partner_rel', 'installation_id', 'partner_id',
                                                 string='Customers', help='Customers of this installation.'),

        
        'module_ids':     fields.many2many('software_knowledge_base.module', 'module_installation_rel', 'installation_id', 'module_id',
                                                 string='Modules', help='Modules used by this installation.'),
                        
        'external_component_ids': fields.many2many('software_knowledge_base.external_component', 'installation_ext_comp_rel', 'installation_id', 'ext_comp_id',
                                                 string='External components',help='Libraries and other third party components used by this installation.'),

        'data_copied_to_m2m': fields.boolean('Partner data moved to new m2m field', groups='base.group_system'),
    }
    
    _defaults = {
        'state': 'setup',
    }
