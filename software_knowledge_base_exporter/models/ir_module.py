import logging
import xmlrpc.client
from datetime import datetime, timedelta

from odoo import models
from odoo.tools import config

_logger = logging.getLogger(__name__)


class Module(models.Model):
    _inherit = "ir.module.module"

    def export_information_to_swkb(self):
        # Get list of installed apps
        apps = self.search([("state", "=", "installed")])
        apps_list = []

        for app in apps:
            apps_list.append(
                {
                    "name": app.name,
                    "description": app.shortdesc,
                    "summary": app.summary,
                    "author": app.author,
                    "website": app.website,
                }
            )

        # Get total users and active users
        users = self.env["res.users"].search([])
        active_users = users.filtered(
            lambda user: user.login_date
            and user.login_date > (datetime.now() - timedelta(weeks=8))
        )

        ir_config = self.env["ir.config_parameter"].sudo()
        url = ir_config.get_param("web.base.url")
        swkb_server = ir_config.get_param("swkb_server")
        swkb_user = ir_config.get_param("swkb_user")
        swkb_token = ir_config.get_param("swkb_token")
        swkb_db = ir_config.get_param("swkb_db")

        odoo_config = config.options
        installation_info = {
            "db_connections_used": odoo_config.get("db_maxconn"),
            "user_accounts_active": len(active_users),
            "user_accounts_total": len(users),
        }

        values = {
            "url": url,
            "module_ids": apps_list,
            "installation_info": installation_info,
        }

        # Database size
        self.env.cr.execute("SELECT pg_database_size(current_database());")
        values["database_total_size_bytes"] = str(int(self.env.cr.fetchall()[0][0]))

        # Attachment size
        values["attachments_total_size_bytes"] = str(sum(
            self.env["ir.attachment"].search([]).mapped("file_size")
        ))

        # Backup size
        if ir_config.get_param("backup_total_size_bytes"):
            values["backup_total_size_bytes"] = str(ir_config.get_param(
                "backup_total_size_bytes"
            ))

        _logger.debug(values)

        common = xmlrpc.client.ServerProxy(f"{swkb_server}/xmlrpc/2/common")
        uid = common.authenticate(swkb_db, swkb_user, swkb_token, {})
        models = xmlrpc.client.ServerProxy(f"{swkb_server}/xmlrpc/2/object")
        models.execute_kw(
            swkb_db,
            uid,
            swkb_token,
            "software_knowledge_base.installation",
            "update_info",
            [url],
            values,
        )
