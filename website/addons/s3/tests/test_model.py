from nose.tools import *
import mock
from boto.s3.connection import *

from tests.base import DbTestCase
from tests.factories import UserFactory, ProjectFactory

from website.addons.s3.model import AddonS3NodeSettings, AddonS3UserSettings


class TestCallbacks(DbTestCase):

    def setUp(self):

        super(TestCallbacks, self).setUp()

        self.project = ProjectFactory.build()
        self.non_authenticator = UserFactory()
        self.project.add_contributor(
            contributor=self.non_authenticator,
            user=self.project.creator,
        )
        self.project.save()

        self.project.add_addon('s3')
        self.project.creator.add_addon('s3')
        self.node_settings = self.project.get_addon('s3')
        self.user_settings = self.project.creator.get_addon('s3')
        self.user_settings.access_key = 'We-Will-Rock-You'
        self.user_settings.secret_key = 'Idontknowanyqueensongs'
        self.node_settings.bucket = 'Sheer-Heart-Attack'
        self.node_settings.user_settings = self.user_settings
        self.node_settings.save()

    @mock.patch('website.addons.s3.model.get_bucket_drop_down')
    def test_node_settings_empty_bucket(self, mock_drop):
        mock_drop.return_value = ''
        s3 = AddonS3NodeSettings()
        assert_equals(s3.to_json(self.project.creator)['has_bucket'], 0)

    @mock.patch('website.addons.s3.model.get_bucket_drop_down')
    def test_node_settings_full_bucket(self, mock_drop):
        mock_drop.return_value = ''
        s3 = AddonS3NodeSettings()
        s3.bucket = 'bucket'
        assert_equals(s3.to_json(self.project.creator)['has_bucket'], 1)

    @mock.patch('website.addons.s3.model.get_bucket_drop_down')
    def test_node_settings_user_auth(self, mock_drop):
        mock_drop.return_value = ''
        s3 = AddonS3NodeSettings()
        assert_equals(s3.to_json(self.project.creator)['user_has_auth'], 1)

    @mock.patch('website.addons.s3.model.get_bucket_drop_down')
    def test_node_settings_moar_use(self, mock_drop):
        mock_drop.return_value = ''
        assert_equals(self.node_settings.to_json(
            self.project.creator)['user_has_auth'], 1)

    def test_user_settings(self):
        s3 = AddonS3UserSettings()
        s3.access_key = "Sherlock"
        s3.secret_key = "lives"
        assert_equals(s3.to_json(self.project.creator)['has_auth'], 1)

    def test_after_fork_authenticator(self):
        fork = ProjectFactory()
        clone, message = self.node_settings.after_fork(self.project,
                                                       fork, self.project.creator)
        assert_equal(self.node_settings.user_settings, clone.user_settings)

    def test_after_fork_not_authenticator(self):
        fork = ProjectFactory()
        clone, message = self.node_settings.after_fork(
            self.project, fork, self.non_authenticator,
        )
        assert_equal(clone.user_settings, None)

    @mock.patch('website.addons.s3.utils.get_bucket_list')
    def test_drop_down_disabled(self, mock_drop):
        bucket = mock.create_autospec(Bucket)
        bucket.name = 'Aticus'
        mock_drop.return_value = [bucket]
        drop_list = self.node_settings.to_json(self.project.creator)['bucket_list']
        assert_true('Aticus' in drop_list)

    @mock.patch('website.addons.s3.model.serialize_bucket')
    @mock.patch('website.addons.s3.model.S3Wrapper.from_addon')
    @mock.patch('website.addons.s3.model.enable_versioning')
    def test_registration(self, mock_wrapper, mock_bucket, mock_versioning):
        mock_versioning.return_value = True
        mock_wrapper.return_value = None
        mock_bucket.return_value = {'Not None': 'None'}
        fork = ProjectFactory()
        clone, message = self.node_settings.after_register(
            self.project, fork, self.project.creator,
        )
        assert_true(clone.is_registration)

    def test_after_remove_contributor(self):
        self.node_settings.after_remove_contributor(
            self.project, self.project.creator
        )
        assert_equal(self.node_settings.user_settings, None)
