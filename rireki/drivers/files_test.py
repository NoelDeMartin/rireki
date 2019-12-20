import os

from rireki.core.project import Project
from rireki.drivers.files import Files
from rireki.testing.test_case import TestCase

try:
    from unittest.mock import ANY, Mock, patch
except ImportError:
    from mock import ANY, Mock, patch


class TestBackup(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self.driver = Files()
        self.driver.project = Project(self.faker.name(), Mock(), Mock())

    @patch('shutil.make_archive')
    @patch('shutil.get_archive_formats')
    def test_uses_zip_when_available(self, get_archive_formats, make_archive):
        # Prepare
        path = '/tmp/' + self.driver.project.slug
        self.driver.load_config({
            'frequency': 42,
            'path': path,
        })
        get_archive_formats.return_value = tuple([tuple(['zip'])])

        # Execute
        self.driver.perform_backup()

        # Assert
        make_archive.assert_called_once_with(ANY, 'zip', path)

        backup_path = os.path.dirname(make_archive.call_args[0][0])
        self.driver.project.storage.upload_backup_files.assert_called_once_with(backup_path)

    @patch('shutil.make_archive')
    @patch('shutil.get_archive_formats')
    def test_uses_tar_fallback(self, get_archive_formats, make_archive):
        # Prepare
        path = '/tmp/' + self.driver.project.slug
        self.driver.load_config({
            'frequency': 42,
            'path': path,
        })
        get_archive_formats.return_value = tuple()

        # Execute
        self.driver.perform_backup()

        # Assert
        make_archive.assert_called_once_with(ANY, 'tar', path)

        backup_path = os.path.dirname(make_archive.call_args[0][0])
        self.driver.project.storage.upload_backup_files.assert_called_once_with(backup_path)
