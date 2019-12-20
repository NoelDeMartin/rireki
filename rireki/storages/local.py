import click
import os

from rireki.core.storage import Storage
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

        return sorted(os.listdir(self.path), reverse=True)

    def _upload_file(self, folder_name, file):
        root_path = os.path.join(self.path, folder_name)

        if not os.path.exists(root_path):
            os.makedirs(root_path)

        copyfile(file, os.path.join(root_path, os.path.basename(file)))

    def __ask_path(self):
        return click.prompt('What is the path?')
