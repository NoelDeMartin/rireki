import os
from shutil import copyfile, rmtree

import click

from rireki.core.store import Store


class Local(Store):
    NAME = 'local'

    def __init__(self):
        Store.__init__(self)

        self.path = None

    def ask_config(self):
        Store.ask_config(self)

        self.path = self._ask_path()

    def load_config(self, config):
        Store.load_config(self, config)

        self.path = config['path']

    def get_config(self):
        config = Store.get_config(self)

        config['path'] = self.path

        return config

    def remove_backup(self, backup):
        path = os.path.join(self.path, backup.filename)

        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)

    def _get_backup_filenames(self):
        if not os.path.exists(self.path):
            return []

        return sorted(os.listdir(self.path), reverse=True)

    def _upload_file(self, source, destination):
        destination = os.path.join(self.path, destination)
        destination_parent = os.path.dirname(destination)

        if not os.path.exists(destination_parent):
            os.makedirs(destination_parent)

        copyfile(source, destination)

    def _ask_path(self):
        return click.prompt('Where do you want to store the backup files?')
