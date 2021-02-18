# 1. Standard library imports:
import logging

import requests

# 2. Known third party imports:
from lxml.html import fromstring
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 3. Odoo imports:
from odoo import _, api, fields, models

from odoo.addons.queue_job.job import job

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
_logger = logging.getLogger(__name__)


class SWKBInstallation(models.Model):
    # 1. Private attributes
    _inherit = "software_knowledge_base.installation"

    # 2. Fields declaration
    url_poll = fields.Boolean(
        string="URL polling",
        default=False,
        help="Periodically poll the url and alert if no response is got",
    )

    url_poll_timeout = fields.Float(string="URL Polling timeout", default=5.0,)

    verify_ssl = fields.Boolean(string="Verify SSL", default=True,)

    installation_poll_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation_poll",
        inverse_name="installation_id",
        string="URL polling",
    )

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @job
    def action_get_website_status(self):
        installation_poll = self.env["software_knowledge_base.installation_poll"]

        s = requests.Session()

        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )

        s.mount("http://", HTTPAdapter(max_retries=retries))

        for record in self:
            url = record.url

            if not url:
                msg = _("URL not set for {}".format(record.name))
                record.message_post(
                    message_type="comment", subtype="mt_comment", body=msg,
                )

            # Add http, if necessary
            if url.find("http") == -1:
                url = "http://%s" % url

            msg = False
            poll = {
                "name": url,
                "installation_id": record.id,
            }

            _logger.debug(_("Trying to open {}".format(url)))
            try:
                response = s.get(
                    url, timeout=record.url_poll_timeout, verify=record.verify_ssl
                )
                tree = fromstring(response.content)
                title = tree.findtext(".//title")
                poll["title"] = title
                poll["content"] = response.content
                poll["status_code"] = response.status_code
                poll["delay"] = response.elapsed.total_seconds()
                poll["timeout"] = record.url_poll_timeout
                poll["success"] = response.status_code == 200
                installation_poll.create(poll)

                if response.status_code != 200:
                    msg = _(
                        "Could not fetch website {}: [{}] {} ".format(
                            url, response.status_code, title
                        )
                    )

            except Exception as e:
                msg = _("Could not fetch website {}: {}".format(url, e))

                poll["description"] = e
                poll["success"] = False
                poll["timeout"] = record.url_poll_timeout

                record.installation_poll_ids = [(0, 0, poll)]

            # Error message is set, and this is the second failed fetch
            # This allows one failed fetch, which will reduce the number of
            # false warning messages
            if (
                msg
                and len(record.installation_poll_ids) > 1
                and not record.installation_poll_ids[1].success
            ):
                record.message_post(
                    message_type="comment", subtype="mt_comment", body=msg,
                )

    # 8. Business methods
    @api.model
    def cron_url_poll(self):
        installations = self.search([("url_poll", "=", True)])

        for installation in installations:
            job_desc = _("SWKB URL Poll for '%s'" % installation.name)
            installation.with_delay(description=job_desc).action_get_website_status()
