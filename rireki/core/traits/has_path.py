import click


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
        return click.prompt('What is the path?')
