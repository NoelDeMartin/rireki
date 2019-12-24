import os

from rireki.core.project import Project
from rireki.drivers.files import Files
from rireki.storages.local import Local
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch
from rireki.utils.string_helpers import str_slug
from rireki.utils.time_helpers import now


class TestFiles(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self.driver = Files()
        self.storage = Local()
        self.project = Project(self.faker.name(), self.driver, self.storage)

        self.driver.project = self.project
        self.storage.project = self.project

    def test_creates_backups_with_one_path(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        storage_path = os.path.join(tmp_path, 'backups')
        driver_paths = [os.path.join(tmp_path, 'files')]

        self.storage.load_config({'path': storage_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': driver_paths,
        })

        touch(os.path.join(driver_paths[0], str_slug(self.faker.word())))

        # Execute
        self.driver.perform_backup()

        # Assert
        assert os.path.exists(storage_path)

        backup = self.storage.get_last_backup()
        assert backup is not None

        assert os.path.exists(os.path.join(storage_path, backup.name, 'backup.zip'))

    def test_creates_backups_with_multiple_paths(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        storage_path = os.path.join(tmp_path, 'backups')
        driver_paths = [
            os.path.join(tmp_path, 'files-1'),
            os.path.join(tmp_path, 'files-2'),
        ]

        self.storage.load_config({'path': storage_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': driver_paths,
        })

        touch(os.path.join(driver_paths[0], str_slug(self.faker.word())))
        touch(os.path.join(driver_paths[1], str_slug(self.faker.word())))

        # Execute
        self.driver.perform_backup()

        # Assert
        assert os.path.exists(storage_path)

        backup = self.storage.get_last_backup()
        assert backup is not None

        assert os.path.exists(os.path.join(storage_path, backup.name, 'backup.zip'))
