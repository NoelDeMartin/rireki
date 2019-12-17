import click


class HasCommand():

    def __init__(self):
        self.command = None

    def ask_config(self):
        self.command = self.__ask_command()

    def load_config(self, config):
        self.command = config['command']

    def get_config(self):
        return {'command': self.command}

    def __ask_command(self):
        return click.prompt('Enter the command you want to execute to perform backups')
