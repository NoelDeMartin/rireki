import click
import os
import shutil

from rireki.core.driver import Driver


class Files(Driver):
    NAME = 'files'

    def __init__(self):
        Driver.__init__(self)

        self.path = None

    def ask_config(self):
        Driver.ask_config(self)

        self.path = self.__ask_path()

    def load_config(self, config):
        Driver.load_config(self, config)

        self.path = config['path']

    def get_config(self):
        config = Driver.get_config(self)

        config['path'] = self.path

        return config

    def _prepare_backup_files(self, path):
        supported_formats = [format[0] for format in shutil.get_archive_formats()]
        format = 'zip' if 'zip' in supported_formats else 'tar'

        shutil.make_archive(os.path.join(path, 'backup'), format, self.path)

    def __ask_path(self):
        return click.prompt('What is the path?')
