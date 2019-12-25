import os

from mock import patch, Mock, ANY
from rireki.core.project import Project
from rireki.stores.digital_ocean import DigitalOcean
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch
from rireki.utils.string_helpers import str_slug
from rireki.utils.time_helpers import now


class TestDigitalOcean(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self.store = DigitalOcean()
        self.project = Project(self.faker.name(), None, self.store)

        self.store.project = self.project

    @patch('boto3.client')
    def test_get_files(self, client):
        # Prepare
        region = self.faker.word()
        access_key = self.faker.sentence()
        access_secret = self.faker.sentence()
        bucket = self.faker.word()
        path = str_slug(self.faker.word())

        self.store.load_config({
            'region': region,
            'access_key': access_key,
            'access_secret': access_secret,
            'bucket': bucket,
            'path': path,
        })

        mock_client = Mock()
        mock_paginator = Mock()
        client.return_value = mock_client
        mock_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = [
            {
                'Contents': [
                    {'Key': os.path.join(path, str(now()))},
                ],
            },
        ]

        # Execute
        backup = self.store.get_last_backup()

        # Assert
        assert backup is not None

        client.assert_called_once_with(
            's3',
            region_name=region,
            endpoint_url='https://%s.digitaloceanspaces.com' % region,
            aws_access_key_id=access_key,
            aws_secret_access_key=access_secret,
        )

        mock_client.get_paginator.assert_called_once_with('list_objects')
        mock_paginator.paginate.assert_called_once_with(Bucket=bucket, Prefix=path)

    @patch('boto3.client')
    def test_upload_files(self, client):
        # Prepare
        region = self.faker.word()
        access_key = self.faker.sentence()
        access_secret = self.faker.sentence()
        bucket = self.faker.word()
        path = str_slug(self.faker.word())
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        placeholder_file_name = str_slug(self.faker.word())
        placeholder_file_path = os.path.join(tmp_path, placeholder_file_name)

        self.store.load_config({
            'region': region,
            'access_key': access_key,
            'access_secret': access_secret,
            'bucket': bucket,
            'path': path,
        })

        touch(placeholder_file_path)

        mock_client = Mock()
        client.return_value = mock_client

        # Execute
        self.store.create_backup(tmp_path)

        # Assert
        client.assert_called_once_with(
            's3',
            region_name=region,
            endpoint_url='https://%s.digitaloceanspaces.com' % region,
            aws_access_key_id=access_key,
            aws_secret_access_key=access_secret,
        )

        mock_client.upload_file.assert_called_once_with(
            placeholder_file_path,
            bucket,
            ANY,
        )

        assert mock_client.upload_file.call_args[0][2].startswith(path)
        assert mock_client.upload_file.call_args[0][2].endswith(placeholder_file_name)
