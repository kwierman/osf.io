# -*- coding: utf-8 -*-

from modularodm import fields

from framework.exceptions import HTTPError

from website.addons.base import AddonUserSettingsBase, AddonNodeSettingsBase
from website.addons.base import StorageAddonBase

from website.addons.dryad import settings as dryad_settings

from website.util import api_url_for


class AddonDryadUserSettings(AddonUserSettingsBase):

    @property
    def has_auth(self):
        return True


class AddonDryadNodeSettings(StorageAddonBase, AddonNodeSettingsBase):
    """
        A Dryad node is a collection of packages. Each package is specified by a DOI, and the title is saved automatically
    """
    dryad_package_doi = fields.StringField()
    complete = True
    has_auth = True
    provider_name = 'dryad'

    user_settings = fields.ForeignField(
        'addondryadusersettings', backref='authorized'
    )

    def delete(self, **kwargs):
        self.dryad_package_doi = None
        super(AddonDryadNodeSettings, self).delete()

    @property
    def folder_name(self):
        #get the name from dryad
        return ''

    def serialize_waterbutler_credentials(self):
        return {'storage': {}}

    def serialize_waterbutler_settings(self):
        ret = dryad_settings.WATERBUTLER_SETTINGS
        #modify the settings here.
        ret['doi'] = self.dryad_package_doi
        return ret

    def create_waterbutler_log(self, auth, action, metadata):
        path = metadata['path']
        url = self.owner.web_url_for('addon_view_or_download_file', path=path, provider='dryad')
        if not metadata.get('extra'):
            sha = None
            urls = {}
        else:
            sha = metadata['extra']['commit']['sha']
            urls = {
                'view': '{0}?ref={1}'.format(url, sha),
                'download': '{0}?action=download&ref={1}'.format(url, sha)
            }

        self.owner.add_log(
            'dryad_{0}'.format(action),
            auth=auth,
            params={
                'project': self.owner.parent_id,
                'node': self.owner._id,
                'path': path,
                'urls': urls,
            },
        )

    def deauthorize(self, auth):
        """Remove user authorization from this node and log the event."""
        self.user_settings = None

    def set_doi(self, doi, title, auth):
        if check_dryad_doi(doi):
            self.dryad_package_doi = doi
            return True
        return False


        self.owner.add_log(
            action='dryad_doi_set',
            params={
                'project': self.owner.parent_id,
                'node': self.owner._id,
                'dryad': {'doi': self.dryad_package_doi, 'title': title}
            },
            auth=auth
        )

    def add_url_to_json(self, js, view_name):
        js.update({view_name: self.owner.api_url_for(view_name)})

    def to_json(self, user):
        ret = super(AddonDryadNodeSettings, self).to_json(user)

        api_endpoints = ['dryad_validate_doi_url',
                'dryad_set_doi_url',
                'dryad_unset_doi_url',
                'dryad_list_objects',
                'dryad_search_objects']

        ret.update({'dryad_package_doi': self.dryad_package_doi if self.dryad_package_doi else ''})
        for endpoint in api_endpoints:
            self.add_url_to_json(ret, endpoint)

        return ret