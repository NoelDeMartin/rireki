import os
import click

from rireki.lib.driver import Driver


class Zip(Driver):
    NAME = 'zip'

    def __init__(self):
        super(Zip, self).__init__(self.NAME)

        self.path = None

    def ask_config(self):
        super(Zip, self).ask_config()

        self.path = self.ask_path()

    def read_config(self, config):
        super(Zip, self).read_config(config)

        self.path = config['path']

    def config(self):
        config = super(Zip, self).config()

        config['path'] = self.path

        return config

    def ask_path(self):
        while True:
            path = click.prompt('What is the path that you want to zip?')

            if not os.path.exists(path):
                click.echo('Path %s doesn\'t exist!' % path)
                continue

            return path
