# -*- coding: utf-8 -*-

from modularodm import fields

from framework.exceptions import HTTPError

from website.util import api_url_for

from website.addons.base import AddonUserSettingsBase, AddonNodeSettingsBase
from website.addons.base import StorageAddonBase

from website.addons.dryad import settings as dryad_settings
from website.addons.dryad import utils as dryad_utils


class AddonDryadUserSettings(AddonUserSettingsBase):
    has_auth=True


class AddonDryadNodeSettings(StorageAddonBase, AddonNodeSettingsBase):
    """
        A Dryad node is a collection of packages. Each package is specified by a DOI, and the title is saved automatically
    """
    dryad_package_doi = fields.StringField()
    complete = True
    has_auth = True
    provider_name = 'dryad'
    connection = dryad_utils.DryadRepository()

    user_settings = fields.ForeignField(
        'addondryadusersettings', backref='authorized'
    )

    def delete(self, **kwargs):
        self.dryad_package_doi = None
        super(AddonDryadNodeSettings, self).delete()

    @property
    def folder_name(self):
        return self.dryad_package_doi

    def serialize_waterbutler_credentials(self):
        return {'storage': {}}

    def serialize_waterbutler_settings(self):
        ret = {}
        ret['doi'] = self.dryad_package_doi
        return ret

    def create_waterbutler_log(self, auth, action, metadata):
        path = metadata['path']
        url = self.owner.web_url_for('addon_view_or_download_file', path=path, provider='dryad')

        self.owner.add_log(
            'dryad_{}'.format(action),
            auth=auth,
            params={
                'project': self.owner.parent_id,
                'node': self.owner._id,
                'path': path,
                'urls': urls,
            },
        )

    def set_doi(self, doi, title, auth):
        if self.connection.check_dryad_doi(doi):
            self.dryad_package_doi = doi
            self.owner.add_log(
                action='dryad_doi_set',
                params={
                    'project': self.owner.parent_id,
                    'node': self.owner._id,
                    'dryad': {'doi': self.dryad_package_doi, 'title': title}
                },
                auth=auth
            )
            return True
        return False

    def add_url_to_json(self, js, view_name):
        js.update({view_name: self.owner.api_url_for(view_name)})

    def to_json(self, user):
        """
            note: The purpose of this definition is mostly to pass the routes in
            this package to the js layer
        """
        ret = super(AddonDryadNodeSettings, self).to_json(user)
        api_endpoints = ['dryad_validate_doi',
                'dryad_settings',
                'dryad_set_doi',
                'dryad_unset_doi',
                'dryad_list_objects',
                'dryad_search_objects',
                'dryad_get_current_metadata']
        ret['urls']={}
        ret.update({'dryad_package_doi': self.dryad_package_doi if self.dryad_package_doi else ''})
        for endpoint in api_endpoints:
            self.add_url_to_json(ret['urls'], endpoint)

        ret['urls'].update({'dryad_page': self.owner.web_url_for('dryad_page')})

        return ret
