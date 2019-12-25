import click
import os

from rireki.core.storage import Storage
from rireki.utils.file_helpers import file_get_name
from shutil import copyfile


class Local(Storage):
    NAME = 'local'

    def __init__(self):
        Storage.__init__(self)

        self.path = None

    def ask_config(self):
        Storage.ask_config(self)

        self.path = self.__ask_path()

    def load_config(self, config):
        Storage.load_config(self, config)

        self.path = config['path']

    def get_config(self):
        config = Storage.get_config(self)

        config['path'] = self.path

        return config

    def _get_backup_names(self):
        if not os.path.exists(self.path):
            return []

        names = []

        for file in os.listdir(self.path):
            names.append(file_get_name(file))

        return sorted(names, reverse=True)

    def _upload_file(self, source, destination):
        destination = os.path.join(self.path, destination)
        destination_parent = os.path.dirname(destination)

        if not os.path.exists(destination_parent):
            os.makedirs(destination_parent)

        copyfile(source, destination)

    def __ask_path(self):
        return click.prompt('Where do you want to store the backup files?')
