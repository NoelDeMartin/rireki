import click
import os


class HasPath():

    def __init__(self):
        self.path = None

    def ask_config(self):
        self.path = self.__ask_path()

    def load_config(self, config):
        self.path = config['path']

    def get_config(self):
        return {'path': self.path}

    def __ask_path(self):
        while True:
            path = click.prompt('What is the path to store backups?')

            if not os.path.exists(path):
                click.echo('Path %s doesn\'t exist!' % path)
                continue

            return path
