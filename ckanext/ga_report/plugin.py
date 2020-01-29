import logging

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckanext.ga_report.views as views

import ckanext.ga_report.helpers as helpers

log = logging.getLogger('ckanext.ga-report')


class GAReportPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IRoutes)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'public')

    # ITemplateHelpers

    def get_helpers(self):
        return helpers.get_helpers()

    # IBlueprint
    def get_blueprint(self):
        return views.get_blueprints()
