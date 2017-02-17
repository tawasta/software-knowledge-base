# -*- coding: utf-8 -*-

# 1. Standard library imports:
import urllib2

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBRepository(models.Model):
    # 1. Private attributes
    _inherit = 'software_knowledge_base.repository'

    # 2. Fields declaration
    #readme = fields.Text(compute='_get_readme', store=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.depends('url', 'vcs_host', 'vcs_team', 'master_branch')
    def _get_readme(self):
        return False

        target_urls = self._get_readme_urls()

        readme = str()
        http_response = {}

        for target_url in target_urls:
            try:
                http_response = urllib2.urlopen(target_url)
            except urllib2.HTTPError:
                self.readme = "README NOT FOUND"

        for line in http_response:
            readme += line

        self.readme = readme

    def _get_readme_urls(self):
        vcs_host = self.vcs_host.name

        filenames = ['README.md', 'README.rst', 'README.txt']
        url_prefix = self.url

        target_urls = []

        for filename in filenames:
            if vcs_host == 'Github':
                url_prefix = "%s/%s/%s" % ("https://raw.githubusercontent.com",
                                           self.vcs_team.name, self.name)
                url_suffix = "/%s/%s" % (self.master_branch, filename)

            elif vcs_host == 'Gitlist':
                url_suffix = "/raw/" + self.master_branch + "/" + filename

            else:
                url_suffix = ""

            if url_prefix and url_suffix:
                target_urls.append(url_prefix + url_suffix)

        return target_urls
