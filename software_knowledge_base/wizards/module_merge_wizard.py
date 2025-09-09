import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ModuleMergeWizard(models.TransientModel):
    _name = "module.merge.wizard"
    _description = "Module Merge Wizard"

    module_ids = fields.Many2many(
        "software_knowledge_base.module",
        string="Modules to Merge",
        required=True,
    )

    target_module_id = fields.Many2one(
        "software_knowledge_base.module",
        string="Target Module",
        required=True,
        help="The module that will remain",
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_ids = self.env.context.get("active_ids")
        if "module_ids" in fields and active_ids:
            res["module_ids"] = [(6, 0, active_ids)]
            res["target_module_id"] = active_ids[0]
        return res

    @api.constrains("module_ids", "target_module_id")
    def _check_target_module_id(self):
        for wizard in self:
            if wizard.target_module_id not in wizard.module_ids:
                raise UserError(_("Target module must be one of the selected modules."))

    def action_merge_modules(self):
        self.ensure_one()

        if len(self.module_ids) > 3:
            raise UserError(_("You can only merge up to 3 modules at a time."))

        ir_model_fields = self.env["ir.model.fields"].sudo()
        m2m_fields = ir_model_fields.search(
            [
                ("ttype", "=", "many2many"),
                ("relation", "=", "software_knowledge_base.module"),
            ]
        )

        m2o_fields = ir_model_fields.search(
            [
                ("ttype", "=", "many2one"),
                ("relation", "=", "software_knowledge_base.module"),
            ]
        )

        target_module_id = self.target_module_id

        for module in self.module_ids:
            if module == target_module_id:
                # Do nothing for the target module
                continue

            # Move all many2one references to the target module
            # (this effectively merges one-to-many data since o2m is the inverse of m2o)
            for m2o_field in m2o_fields:
                _logger.info(m2o_field.name)
                # Ensure the owning model exists and is not transient (wizards, etc.)
                if not m2o_field.model_id or m2o_field.model_id.transient:
                    continue

                model_name = m2o_field.model_id.model
                field_name = m2o_field.name

                target_model = self.env[model_name].sudo()

                # Safety check: the field must be a many2one to the module model
                fld = target_model._fields.get(field_name)
                if not fld or fld.type != "many2one" or fld.comodel_name != "software_knowledge_base.module":
                    continue

                # Update all records that currently point to the module being merged
                records = target_model.search([(field_name, "=", module.id)])
                if records:
                    records.write({field_name: target_module_id.id})

            # Handle m2m-fields
            for m2m_field in m2m_fields:
                if m2m_field.model_id.transient:
                    # Don't try to merge transient models
                    continue

                target_model = self.env[m2m_field.model_id.model].sudo()
                change_records = target_model.sudo().search(
                    [(m2m_field.name, "=", module.id)]
                )
                for change_record in change_records:
                    change_record.write(
                        {
                            m2m_field.name: [
                                # Delete the old link
                                fields.Command.unlink(module.id),
                                # Add new link
                                fields.Command.link(target_module_id.id),
                            ]
                        }
                    )

            module.unlink()

        return {
            "type": "ir.actions.act_window_close",
        }
