# -*- coding: utf-8 -*-

# 1. Standard library imports:
import urllib2
import logging

# 2. Known third party imports:
from bs4 import BeautifulSoup
from timeit import default_timer as timer

# 3. Odoo imports (openerp):
from openerp import api, fields, models, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
_logger = logging.getLogger(__name__)


class SWKBInstallation(models.Model):
    # 1. Private attributes
    _inherit = 'software_knowledge_base.installation'

    # 2. Fields declaration
    url_poll = fields.Boolean(
        string='URL polling',
        default=False,
        help='Periodically poll the url and alert if no response is got',
    )

    installation_poll_ids = fields.One2many(
        comodel_name='software_knowledge_base.installation_poll',
        inverse_name='installation_id',
        string='URL polling',
    )

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_get_website_status(self):
        for record in self:
            url = record.url

            # Add http, if necessary
            if url.find('http') == -1:
                url = 'http://%s' % url

            poll = {
                'name': url,
                'installation_id': record.id,
            }

            _logger.debug(_('Trying to open {}'.format(url)))
            try:
                start = timer()
                response = urllib2.urlopen(url)
                end = timer()
                delay = (end - start)
                soup = BeautifulSoup(response.read(), 'lxml')

                title = soup.find('title', text=True).contents[0]

                robots = soup.find('meta', {'name': 'robots'})
                if robots:
                    robots = robots.get('content', 'no robots meta')
                else:
                    robots = 'no robots meta'

                content = '{} ({})'.format(title, robots)

                poll['description'] = content
                poll['delay'] = delay
                poll['success'] = True

                record.installation_poll_ids = [(0, 0, poll)]

            except Exception as e:
                msg = _('Could not fetch website {}: {}'.format(url, e))

                poll['description'] = e
                poll['success'] = False

                record.installation_poll_ids = [(0, 0, poll)]

                record.message_post(
                    type='comment',
                    subtype='mt_comment',
                    body=msg,
                )

    # 8. Business methods
    @api.model
    def cron_url_poll(self):
        installations = self.search([
            ('url_poll', '=', True),
        ])

        installations.action_get_website_status()
