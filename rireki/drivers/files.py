import os
import shutil
import tempfile

import click

from rireki.core.driver import Driver
from rireki.core.errors import BackupError


class Files(Driver):
    NAME = 'files'

    def __init__(self):
        Driver.__init__(self)

        self.paths = []

    def ask_config(self):
        Driver.ask_config(self)

        self.paths = self._ask_paths()

    def load_config(self, config):
        Driver.load_config(self, config)

        self.paths = config['paths']

    def get_config(self):
        config = Driver.get_config(self)

        config['paths'] = self.paths

        return config

    def _prepare_backup_files(self, path):
        format = self._get_archive_format()

        with TemporaryBackupFolder(self) as folder:
            shutil.make_archive(os.path.join(path, 'backup'), format, folder.path)

        return os.path.join(path, 'backup.' + format)

    def _ask_paths(self):
        paths = []
        continue_asking = True

        while continue_asking:
            paths.append(self._ask_path())

            continue_asking = click.confirm('Is there anything else you\'d like to back up?')

        return paths

    def _ask_path(self):
        path = None

        while not path:
            path = click.prompt('Where are the files you want to back up?')

            if os.path.exists(path):
                break

            if not click.confirm('There is nothing there, are you sure that\'s the correct path?'):
                path = None

        return path

    def _get_archive_format(self):
        supported_formats = [format[0] for format in shutil.get_archive_formats()]

        return 'zip' if 'zip' in supported_formats else 'tar'


class TemporaryBackupFolder:

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self._check_basename_collisions()

        self.path = tempfile.mkdtemp(
            prefix=f'rireki-files-backup-{self.driver.project.slug}-'
        )

        try:
            self._copy_paths()
        except BaseException:
            self._remove()
            raise

        return self

    def __exit__(self, type, value, traceback):
        self._remove()

    def _copy_paths(self):
        copied = set()

        for path in self.driver.paths:
            normalized_path = os.path.normpath(path)
            if normalized_path in copied:
                continue

            copied.add(normalized_path)
            basename = os.path.basename(normalized_path) or 'root'
            dest_path = os.path.join(self.path, basename)

            if os.path.isdir(normalized_path):
                shutil.copytree(normalized_path, dest_path)
            else:
                shutil.copy2(normalized_path, dest_path)

    def _remove(self):
        shutil.rmtree(self.path, ignore_errors=True)

    def _check_basename_collisions(self):
        seen = {}

        for path in self.driver.paths:
            normalized_path = os.path.normpath(path)
            basename = os.path.basename(normalized_path) or 'root'

            if basename in seen and seen[basename] != normalized_path:
                raise BackupError(
                    f'Basename collision detected between "{seen[basename]}" and "{normalized_path}". '
                    'Paths to back up must have unique basenames.'
                )

            seen[basename] = normalized_path
