# -*- coding: utf-8 -*-
from nose.tools import assert_false, assert_in, assert_true, assert_equal
import mock

import httplib as http
from tests.factories import AuthUserFactory

from website.addons.base.testing.views import OAuthAddonAuthViewsTestCaseMixin
from website.util import api_url_for
from website.addons.base.testing import views
from website.addons.owncloud.model import OwnCloudProvider
from website.addons.owncloud.serializer import OwnCloudSerializer
from website.addons.owncloud.tests.utils import (OwnCloudAddonTestCase)


class TestAuthViews(OAuthAddonAuthViewsTestCaseMixin, OwnCloudAddonTestCase):

    @property
    def Provider(self):
        return OwnCloudProvider

    def test_oauth_start(self):
        pass

    def test_oauth_finish(self):
        pass

    def test_user_config_get(self):
        url = api_url_for('owncloud_user_config_get')
        new_user = AuthUserFactory.build()
        res = self.app.get(url, auth=new_user.auth)

        result = res.json.get('result')
        assert_false(result['userHasAuth'])
        assert_in('hosts', result)
        assert_in('create', result['urls'])

        res = self.app.get(url, auth=self.user.auth)

        result = res.json.get('result')
        assert_true(result['userHasAuth'])


class TestConfigViews(OwnCloudAddonTestCase, views.OAuthAddonConfigViewsTestCaseMixin):
    Serializer = OwnCloudSerializer
    client = OwnCloudProvider

    @property
    def folder(self):
        return {'name': '/Documents/', 'path': '/Documents/'}

    def setUp(self):
        super(TestConfigViews, self).setUp()
        self.mock_ser_api = mock.patch('owncloud.Client.login')
        self.mock_ser_api.start()
        self.set_node_settings(self.node_settings)

    def tearDown(self):
        self.mock_ser_api.stop()
        super(TestConfigViews, self).tearDown()

    @mock.patch('website.addons.owncloud.model.AddonOwnCloudNodeSettings.get_folders')
    def test_folder_list(self, mock_connection):
        #test_get_datasets
        mock_connection.return_value = ['/Documents/', '/Pictures/', '/Videos/']

        super(TestConfigViews, self).test_folder_list()

    def test_get_config(self):
        url = self.project.api_url_for('{0}_get_config'.format(self.ADDON_SHORT_NAME))
        res = self.app.get(url, auth=self.user.auth)
        assert_equal(res.status_code, http.OK)
        assert_in('result', res.json)
        serialized = self.Serializer().serialize_settings(
            self.node_settings,
            self.user,
        )
        assert_equal(serialized, res.json['result'])