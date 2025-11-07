import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CapabilityApplyWizard(models.TransientModel):
    _name = "swkb.capability.apply.wizard"
    _description = "Apply selected capabilities to installation"

    installation_id = fields.Many2one(
        "software_knowledge_base.installation",
        required=True,
        readonly=True,
    )
    line_ids = fields.One2many(
        "swkb.capability.apply.wizard.line",
        "wizard_id",
        string="Capabilities",
    )

    @api.model
    def default_get(self, fields_list):
        """
        Populate wizard with capabilities linked to the
        installation and their resolved modules.
        """
        vals = super().default_get(fields_list)
        installation = None
        if self.env.context.get("default_installation_id"):
            installation = self.env["software_knowledge_base.installation"].browse(
                self.env.context["default_installation_id"]
            )
        vals["installation_id"] = installation.id if installation else False

        lines = []
        if installation:
            for cap in installation.capability_ids:
                module_ids = list(cap._resolve_modules())
                lines.append(
                    (
                        0,
                        0,
                        {
                            "capability_id": cap.id,
                            "module_ids": [(6, 0, module_ids)],
                            "apply": False,
                        },
                    )
                )
        vals["line_ids"] = lines
        return vals

    def action_apply(self):
        """
        Log selected capabilities and their modules
        (hook point for future automation).
        """
        self.ensure_one()
        chosen = self.line_ids.filtered(lambda line: line.apply)
        if not chosen:
            _logger.info(
                "Capabilities apply: no capabilities selected for installation_id=%s",
                self.installation_id.id,
            )
            return {"type": "ir.actions.act_window_close"}

        for line in chosen:
            _logger.info(
                "Capabilities apply: installation_id=%s capability=%s modules=%s",
                self.installation_id.id,
                line.capability_id.display_name,
                ",".join(map(str, line.module_ids.ids)),
            )
        return {"type": "ir.actions.act_window_close"}


class CapabilityApplyWizardLine(models.TransientModel):
    _name = "swkb.capability.apply.wizard.line"
    _description = "Capability selection line"

    wizard_id = fields.Many2one(
        "swkb.capability.apply.wizard",
        required=True,
        ondelete="cascade",
    )
    apply = fields.Boolean(
        help="Select to apply this capability.",
    )
    capability_id = fields.Many2one(
        "swkb.capability",
    )
    module_ids = fields.Many2many(
        "software_knowledge_base.module",
        "skb_cap_apply_wiz_line_module_rel",
        "line_id",
        "module_id",
        string="Modules",
        readonly=True,
    )
