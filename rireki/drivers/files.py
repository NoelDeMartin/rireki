import click
import os
import shutil

from rireki.core.driver import Driver
from rireki.utils.time_helpers import now


class Files(Driver):
    NAME = 'files'

    def __init__(self):
        Driver.__init__(self)

        self.paths = []

    def ask_config(self):
        Driver.ask_config(self)

        self.paths = self.__ask_paths()

    def load_config(self, config):
        Driver.load_config(self, config)

        self.paths = config['paths']

    def get_config(self):
        config = Driver.get_config(self)

        config['paths'] = self.paths

        return config

    def _prepare_backup_files(self, path):
        format = self.__get_archive_format()

        with TemporaryBackupFolder(self) as folder:
            shutil.make_archive(os.path.join(path, 'backup'), format, folder.path)

        return os.path.join(path, 'backup.' + format)

    def __ask_paths(self):
        paths = []
        continue_asking = True

        while continue_asking:
            paths.append(self.__ask_path())

            continue_asking = click.confirm('Is there anything else you\'d like to back up?')

        return paths

    def __ask_path(self):
        path = None

        while not path:
            path = click.prompt('Where are the files you want to back up?')

            if os.path.exists(path):
                break

            if not click.confirm('There is nothing there, are you sure that\'s the correct path?'):
                path = None

        return path

    def __get_archive_format(self):
        supported_formats = [format[0] for format in shutil.get_archive_formats()]

        return 'zip' if 'zip' in supported_formats else 'tar'


class TemporaryBackupFolder():

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.path = os.path.join(
            '/tmp',
            'rireki-files-backup-{}-{}'.format(self.driver.project.slug, now())
        )

        os.makedirs(self.path)

        for path in self.driver.paths:
            shutil.copytree(path, os.path.join(self.path, os.path.basename(path)))

        return self

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.path)
