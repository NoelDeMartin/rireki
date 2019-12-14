import os
import click

from rireki.core.storage import Storage


class Local(Storage):
    NAME = 'local'

    def __init__(self):
        super(Local, self).__init__(self.NAME)

        self.path = None

    def ask_config(self):
        super(Local, self).ask_config()

        self.path = self.ask_path()

    def read_config(self, config):
        super(Local, self).read_config(config)

        self.path = config['path']

    def config(self):
        config = super(Local, self).config()

        config['path'] = self.path

        return config

    def ask_path(self):
        while True:
            path = click.prompt('What is the path to store backups?')

            if not os.path.exists(path):
                click.echo('Path %s doesn\'t exist!' % path)
                continue

            return path
