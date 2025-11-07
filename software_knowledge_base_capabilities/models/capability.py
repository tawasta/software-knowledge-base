from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Capability(models.Model):
    _name = "swkb.capability"
    _description = "Business Capability"
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    active = fields.Boolean(default=True)

    # Requirements (each links one module that this capability needs)
    requirement_ids = fields.One2many(
        "swkb.capability.requirement",
        "capability_id",
        string="Module Requirements",
    )

    # Capability composition (include other capabilities)
    child_capability_ids = fields.Many2many(
        "swkb.capability",
        "skb_capability_component_rel",      # keep original relation table
        "parent_capability_id",
        "child_capability_id",
        string="Included Capabilities",
    )

    # Resolved modules (direct + via included capabilities)
    resolved_module_ids = fields.Many2many(
        "software_knowledge_base.module",
        compute="_compute_resolved_module_ids",
        string="Resolved Modules",
        store=False,
    )

    # -------------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------------
    @api.constrains("child_capability_ids")
    def _check_no_self(self):
        """Prevent a capability from including itself."""
        for rec in self:
            if rec.id and rec.id in rec.child_capability_ids.ids:
                raise ValidationError(_("A capability cannot include itself."))

    @api.constrains("child_capability_ids")
    def _check_no_cycles(self):
        """Prevent cyclic capability composition."""
        def visit(node, seen):
            if node.id in seen:
                return True
            seen = seen | {node.id}
            for child in node.child_capability_ids:
                if visit(child, seen):
                    return True
            return False

        for rec in self:
            if visit(rec, set()):
                raise ValidationError(_("Cyclic capability composition is not allowed."))

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _resolve_modules(self, seen_caps=None):
        """Return a set of module IDs including nested child capabilities."""
        seen_caps = seen_caps or set()
        result = set()
        for rec in self:
            if rec.id in seen_caps:
                continue
            seen_caps.add(rec.id)
            for req in rec.requirement_ids:
                if req.module_id:
                    result.add(req.module_id.id)
            for child in rec.child_capability_ids:
                result |= child._resolve_modules(seen_caps)
        return result

    @api.depends(
        "requirement_ids.module_id",
        "child_capability_ids",
        "child_capability_ids.requirement_ids.module_id",
    )
    def _compute_resolved_module_ids(self):
        """Compute all modules linked directly or indirectly to this capability."""
        for rec in self:
            rec.resolved_module_ids = [(6, 0, list(rec._resolve_modules()))]


class CapabilityRequirement(models.Model):
    _name = "swkb.capability.requirement"
    _description = "Capability Module Requirement"
    _order = "sequence, id"

    capability_id = fields.Many2one(
        "swkb.capability",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(default=10)
    module_id = fields.Many2one(
        "software_knowledge_base.module",
        required=True,
        index=True,
    )
    required = fields.Boolean(
        default=True,
        help="Whether this module is mandatory for the capability.",
    )
    note = fields.Char()
