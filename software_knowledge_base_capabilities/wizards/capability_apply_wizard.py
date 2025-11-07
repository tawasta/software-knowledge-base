import logging
import time
import xmlrpc.client

from odoo import _, api, fields, models
from odoo.exceptions import UserError

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
        """Populate wizard with capabilities and resolved modules."""
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

    # --------------------------- helpers ------------------------------------
    def _pick_first(self, rec, *names):
        """Return first truthy attribute value by name on record, else None."""
        for n in names:
            if hasattr(rec, n):
                val = getattr(rec, n)
                if val:
                    return val
        return None

    def _notify(self, title, message, level="info", sticky=False):
        """Send a webclient toast via bus (works in community).
        level: 'success' | 'warning' | 'danger' | 'info'
        """
        payload = {
            "title": title,
            "message": message,
            "sticky": bool(sticky),
            "type": level,
        }
        # Send to current user only
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id, "simple_notification", payload
        )

    def _get_rpc_credentials(self):
        """Resolve base_url, db, user, key from Installation + system params."""
        self.ensure_one()
        inst = self.installation_id

        base_url = self._pick_first(inst, "admin_url", "url")
        db = self._pick_first(inst, "identifier")
        if not base_url or not db:
            raise UserError(_("Installation is missing admin URL/URL or identifier."))

        icp = self.env["ir.config_parameter"].sudo()
        user = icp.get_param("skb_capabilities.client_user") or "admin"
        key = icp.get_param("skb_capabilities.client_key")
        if not key:
            raise UserError(
                _(
                    "System parameter 'skb_capabilities.client_key' is not set. "
                    "Set it to the client password or API key."
                )
            )
        return str(base_url).rstrip("/"), db, user, key

    # ---------------------------- action ------------------------------------
    def action_apply(self):
        """Auth → notify → wait → notify → resolve modules → install → final notify."""
        self.ensure_one()

        # 1) Collect module technical names from selected lines
        chosen = self.line_ids.filtered(lambda line: line.apply)
        capability_ids = self.env["swkb.capability"].browse(
            [li.capability_id.id for li in chosen]
        )
        module_names = capability_ids.resolved_module_ids.mapped("name")
        module_list_msg = (
            ", ".join(module_names) if module_names else "(no modules selected)"
        )

        # 2) Resolve creds & authenticate
        base_url, db, user, key = self._get_rpc_credentials()
        common = xmlrpc.client.ServerProxy(
            f"{base_url}/xmlrpc/2/common", allow_none=True
        )
        uid = common.authenticate(db, user, key, {})
        if not uid:
            raise UserError(
                f"Authentication failed to {base_url} (db={db}, user={user}). "
                "Check credentials and database name."
            )

        # 3) Notify auth OK (flush immediately)
        self._notify(
            "Connection OK",
            f"Authenticated to {base_url} (db={db}) as {user}.",
            level="success",
        )
        self.env.cr.commit()  # pylint: disable=invalid-commit

        # 4) Quick ping
        obj = xmlrpc.client.ServerProxy(f"{base_url}/xmlrpc/2/object", allow_none=True)
        try:
            _ = obj.execute_kw(
                db,
                uid,
                key,
                "ir.module.module",
                "search_count",
                [[["name", "!=", False]]],
            )
        except Exception as err:
            raise UserError(f"RPC ping failed: {err}") from err

        # 5) Wait ~4s so user sees the step-by-step
        time.sleep(4)

        # 6) Notify starting install (flush)
        self._notify(
            "Installation",
            f"Starting installation… Modules: {module_list_msg}",
            level="info",
        )
        self.env.cr.commit()  # pylint: disable=invalid-commit

        if not module_names:
            self._notify("Nothing to install", "No modules selected.", level="warning")
            self.env.cr.commit()  # pylint: disable=invalid-commit
            return {"type": "ir.actions.act_window_close"}

        # 7) Resolve found/missing and states
        found_ids = obj.execute_kw(
            db,
            uid,
            key,
            "ir.module.module",
            "search",
            [[["name", "in", module_names]]],
        )
        found_modules = []
        if found_ids:
            found_modules = obj.execute_kw(
                db,
                uid,
                key,
                "ir.module.module",
                "read",
                [found_ids, ["name", "state"]],
            )
        found_names = {m["name"] for m in found_modules}
        missing_names = [n for n in module_names if n not in found_names]

        if missing_names:
            self._notify(
                "Missing modules in client",
                f"Not found by technical name: {', '.join(missing_names)}",
                level="warning",
            )
            self.env.cr.commit()  # pylint: disable=invalid-commit

        # Filter to_install: those found AND state != installed
        to_install_ids = [
            m["id"] for m in found_modules if m.get("state") != "installed"
        ]
        already_installed = [
            m["name"] for m in found_modules if m.get("state") == "installed"
        ]

        if already_installed:
            self._notify(
                "Already installed",
                ", ".join(already_installed),
                level="info",
            )
            self.env.cr.commit()  # pylint: disable=invalid-commit

        if not to_install_ids:
            self._notify(
                "Nothing to install",
                "All selected modules are already installed or not found.",
                level="warning",
            )
            self.env.cr.commit()  # pylint: disable=invalid-commit
            return {"type": "ir.actions.act_window_close"}

        # 8) Install (handles dependencies)
        obj.execute_kw(
            db,
            uid,
            key,
            "ir.module.module",
            "button_immediate_install",
            [to_install_ids],
        )

        self._notify(
            "Success",
            "Installation complete. Installed: "
            + ", ".join(
                [m["name"] for m in found_modules if m["id"] in to_install_ids]
            ),
            level="success",
        )
        self.env.cr.commit()  # pylint: disable=invalid-commit

        return {"type": "ir.actions.act_window_close"}


class CapabilityApplyWizardLine(models.TransientModel):
    _name = "swkb.capability.apply.wizard.line"
    _description = "Capability selection line"

    wizard_id = fields.Many2one(
        "swkb.capability.apply.wizard",
        required=True,
        ondelete="cascade",
    )
    apply = fields.Boolean(help="Select to apply this capability.")
    capability_id = fields.Many2one("swkb.capability")
    module_ids = fields.Many2many(
        "software_knowledge_base.module",
        "skb_cap_apply_wiz_line_module_rel",
        "line_id",
        "module_id",
        string="Modules",
        readonly=True,
    )
