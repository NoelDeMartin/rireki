import os

from rireki.core.project import Project
from rireki.drivers.files import Files
from rireki.stores.local import Local
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch
from rireki.utils.string_helpers import str_slug
from rireki.utils.time_helpers import now


class TestFiles(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self.driver = Files()
        self.store = Local()
        self.project = Project(self.faker.name(), self.driver, self.store)

        self.driver.project = self.project
        self.store.project = self.project

    def test_creates_backups_with_one_path(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        driver_paths = [os.path.join(tmp_path, 'files')]

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': driver_paths,
        })

        touch(os.path.join(driver_paths[0], str_slug(self.faker.word())))

        # Execute
        self.driver.perform_backup()

        # Assert
        assert os.path.exists(store_path)

        backup = self.store.get_last_backup()
        assert backup is not None

        assert os.path.exists(os.path.join(store_path, backup.name + '.zip'))

    def test_creates_backups_with_multiple_paths(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        driver_paths = [
            os.path.join(tmp_path, 'files-1'),
            os.path.join(tmp_path, 'files-2'),
        ]

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': driver_paths,
        })

        touch(os.path.join(driver_paths[0], str_slug(self.faker.word())))
        touch(os.path.join(driver_paths[1], str_slug(self.faker.word())))

        # Execute
        self.driver.perform_backup()

        # Assert
        assert os.path.exists(store_path)

        backup = self.store.get_last_backup()
        assert backup is not None

        assert os.path.exists(os.path.join(store_path, backup.name + '.zip'))
