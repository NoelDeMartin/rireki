import os
import tempfile

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

    def test_creates_backups_with_files(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        file_name = str_slug(self.faker.word())
        store_path = os.path.join(tmp_path, 'backups')
        driver_paths = [os.path.join(tmp_path, 'files', file_name)]

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': driver_paths,
        })

        touch(driver_paths[0])

        # Execute
        self.driver.perform_backup()

        # Assert
        assert os.path.exists(store_path)

        backup = self.store.get_last_backup()
        assert backup is not None

        assert os.path.exists(os.path.join(store_path, backup.name + '.zip'))

    def test_creates_backups_with_colliding_directory_basenames_raises_error(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        dir1 = os.path.join(tmp_path, 'site1', 'data')
        dir2 = os.path.join(tmp_path, 'site2', 'data')

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': [dir1, dir2],
        })

        touch(os.path.join(dir1, 'file1.txt'))
        touch(os.path.join(dir2, 'file2.txt'))

        # Execute & Assert
        with self.assertRaises(Exception) as ctx:
            self.driver.perform_backup()

        assert 'Basename collision detected between "{}" and "{}"'.format(dir1, dir2) in str(ctx.exception)

    def test_creates_backups_with_colliding_file_basenames_raises_error(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        file1 = os.path.join(tmp_path, 'site1', 'config.json')
        file2 = os.path.join(tmp_path, 'site2', 'config.json')

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': [file1, file2],
        })

        touch(file1)
        touch(file2)

        # Execute & Assert
        with self.assertRaises(Exception) as ctx:
            self.driver.perform_backup()

        assert 'Basename collision detected between "{}" and "{}"'.format(file1, file2) in str(ctx.exception)

    def test_creates_backups_with_colliding_basenames_normalizes_paths_in_error(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        dir1 = os.path.join(tmp_path, 'site1', 'data')
        dir2 = os.path.join(tmp_path, 'site2', 'data')

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': [dir1 + '/', dir2 + '/'],
        })

        touch(os.path.join(dir1, 'file1.txt'))
        touch(os.path.join(dir2, 'file2.txt'))

        # Execute & Assert
        with self.assertRaises(Exception) as ctx:
            self.driver.perform_backup()

        assert 'Basename collision detected between "{}" and "{}"'.format(dir1, dir2) in str(ctx.exception)

    def test_creates_backups_handles_trailing_slashes(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        driver_paths = [os.path.join(tmp_path, 'files') + '/']

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': driver_paths,
        })

        touch(os.path.join(tmp_path, 'files', str_slug(self.faker.word())))

        # Execute
        self.driver.perform_backup()

        # Assert
        assert os.path.exists(store_path)
        backup = self.store.get_last_backup()
        assert backup is not None
        assert os.path.exists(os.path.join(store_path, backup.name + '.zip'))

    def test_creates_backups_handles_duplicate_paths(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        dir_path = os.path.join(tmp_path, 'files')
        driver_paths = [dir_path, dir_path + '/']

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': driver_paths,
        })

        touch(os.path.join(dir_path, str_slug(self.faker.word())))

        # Execute
        self.driver.perform_backup()

        # Assert
        assert os.path.exists(store_path)
        backup = self.store.get_last_backup()
        assert backup is not None
        assert os.path.exists(os.path.join(store_path, backup.name + '.zip'))

    def test_creates_backups_with_missing_path_cleans_up_temporary_folder(self):
        # Prepare
        tmp_path = os.path.join(self.home_path, '{}-{}'.format(self.project.slug, now()))
        store_path = os.path.join(tmp_path, 'backups')
        existing_path = os.path.join(tmp_path, 'existing')
        missing_path = os.path.join(tmp_path, 'missing')
        tmp_prefix = 'rireki-files-backup-{}-'.format(self.project.slug)

        self.store.load_config({'path': store_path})
        self.driver.load_config({
            'frequency': 42,
            'paths': [existing_path, missing_path],
        })

        touch(os.path.join(existing_path, str_slug(self.faker.word())))

        # Execute & Assert
        with self.assertRaises(FileNotFoundError):
            self.driver.perform_backup()

        leaked_folders = [name for name in os.listdir(tempfile.gettempdir()) if name.startswith(tmp_prefix)]
        assert leaked_folders == []
        assert not os.path.exists(store_path)
