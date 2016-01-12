#!/usr/bin/env python
# encoding: utf-8

import mock
import unittest
import httpretty
from os.path import join as join_path
from json import dumps

from nose.tools import *  # noqa

from framework.auth import Auth

from tests.test_addons import assert_urls_equal

from website.addons.dryad import views
from website.addons.dryad import utils
from website.addons.dryad.views import *
from website.util import api_url_for, web_url_for

from nose.tools import *  # noqa

from website.addons.dryad.tests.utils import *
from website.addons.dryad.utils import DryadRepository


class TestJSONViews(DryadTestCase):
    """
        TODO: Add in unit tests for browse and search calls. This is a
        bit challenging as there are A LOT of dryad API calls for these two.
        This might call for a refactor of the knockout code
    """

    def setUp(self):
        super(DryadTestCase, self).setUp()
        self.user = AuthUserFactory()
        self.project = ProjectFactory(creator=self.user)
        self.project.add_addon('dryad', auth=Auth(self.user))
        self.project.creator.add_addon('dryad')
        self.node_settings = self.project.get_addon('dryad')
        self.user_settings = self.project.creator.get_addon('dryad')
        self.user_settings.save()
        self.node_settings.user_settings = self.user_settings
        self.node_settings.save()
        #self.connection = DryadTestConnection()
        #self.repository = DryadTestRepository(self.connection)
        #self.node_settings.connection = self.repository

    @httpretty.activate
    def test_validate_doi(self):
        httpretty.register_uri(
            httpretty.GET,
            dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850'),
            status=200
        )
        httpretty.register_uri(
            httpretty.GET,
            dryad_settings.DRYAD_DATAONE_METADATA.format('NOTADOI'),
            status=404
        )
        url = '/api/v1/project/{}/dryad/validate'.format(self.project._id)
        resp = self.app.get(url, auth=self.user.auth, params={'doi': 'doi:10.5061/dryad.1850'})
        assert_true(resp.json)
        resp = self.app.get(url, auth=self.user.auth, params={'doi': 'NOTADOI'})
        assert_false(resp.json)

    @httpretty.activate
    def test_dryad_set_doi(self):
        httpretty.register_uri(
            httpretty.GET,
            dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850'),
            body=response_dict[dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850')]
        )
        url = '/api/v1/project/{}/dryad/set'.format(self.project._id)
        doi ='doi:10.5061/dryad.1850'
        self.app.post(url, auth=self.user.auth, params={'doi': doi})
        settings = self.node_settings
        settings.reload()
        assert_equal(settings.dryad_package_doi,doi)

    @httpretty.activate
    def test_dryad_settings(self):
        httpretty.register_uri(
            httpretty.GET,
            dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850'),
            body=response_dict[dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850')]
        )
        url = '/api/v1/project/{}/dryad/set'.format(self.project._id)
        settings = self.node_settings
        doi ='doi:10.5061/dryad.1850'
        resp = self.app.post(url, auth=self.user.auth, params={'doi': doi})
        assert_true(resp.json)
        url='/api/v1/project/{}/dryad/settings'.format(self.project._id)
        settings_resp = self.app.get(url, auth=self.user.auth)
        assert_equal(settings_resp.json['dryad_package_doi'],doi)

    @httpretty.activate
    def test_dryad_get_current_metadata(self):
        test_url  =dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850')
        httpretty.register_uri(
            httpretty.GET,
            dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850'),
            responses=[
               httpretty.Response(body="Response to Set DOI", status=200),
               httpretty.Response(body=response_dict[dryad_settings.DRYAD_DATAONE_METADATA.format('doi:10.5061/dryad.1850')],
                    status=200),
            ]
        )
        settings = self.node_settings
        assert_true(settings.set_doi('doi:10.5061/dryad.1850', "My Title",auth=Auth(self.user) ))
        assert_equal(settings.dryad_package_doi,'doi:10.5061/dryad.1850')
        settings.save()
        url = '/api/v1/project/{}/dryad/metadata'.format(self.project._id)
        meta_resp = self.app.get(url, auth=self.user.auth)
        assert_true(meta_resp.json['doi']=='doi:10.5061/dryad.1850')

    def test_dryad_unset_doi(self):
        settings = self.node_settings
        assert_true(dryad_unset_doi(pid=self.project._id, auth=Auth(self.user)))
        settings.reload()
        assert_is_none(self.node_settings.dryad_package_doi)


class TestWebViews(DryadTestCase):

    def setUp(self):
        super(DryadTestCase, self).setUp()
        self.user = AuthUserFactory()
        self.project = ProjectFactory(creator=self.user)
        self.project.add_addon('dryad', auth=Auth(self.user))
        self.project.creator.add_addon('dryad')
        self.node_settings = self.project.get_addon('dryad')
        self.user_settings = self.project.creator.get_addon('dryad')
        self.user_settings.save()
        self.node_settings.user_settings = self.user_settings
        self.node_settings.save()
        self.connection = DryadTestConnection()
        self.repository = DryadTestRepository(self.connection)
        self.node_settings.connection = self.repository

    @unittest.skip('finish the browser unit tests in utils first')
    def test_dryad_page(self):
        url = '/api/v1/project/{}/dryad/'.format(self.project._id)
        self.app.get(url, auth=self.user.auth)
        assert True

class TestUtilViews(DryadTestCase):

    def setUp(self):
        super(DryadTestCase, self).setUp()
        self.user = AuthUserFactory()
        self.project = ProjectFactory(creator=self.user)
        self.project.add_addon('dryad', auth=Auth(self.user))
        self.project.creator.add_addon('dryad')
        self.node_settings = self.project.get_addon('dryad')
        self.user_settings = self.project.creator.get_addon('dryad')
        self.user_settings.save()
        self.node_settings.user_settings = self.user_settings
        self.node_settings.save()
        self.connection = DryadTestConnection()
        self.repository = DryadTestRepository(self.connection)
        self.node_settings.connection = self.repository


    def test_hgrid_view(self):
        #test the hgrid without any doi
        ref = dryad_addon_folder(self.node_settings, self.user.auth)
        assert_equal(ref, [])
        #now add a doi
        settings = self.node_settings
        assert_true(settings.set_doi('doi:10.5061/dryad.1850', "My Title",auth=Auth(self.user) ))
        assert_equal(settings.dryad_package_doi,'doi:10.5061/dryad.1850')
        settings.save()
        ref = dryad_addon_folder(self.node_settings, auth=Auth(self.user))
        assert_false(ref==[])
