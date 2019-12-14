import click

from rireki.core.driver import Driver


class Custom(Driver):
    NAME = 'custom'

    def __init__(self):
        super(Custom, self).__init__(self.NAME)

    def ask_config(self):
        super(Custom, self).ask_config()

        self.command = self.ask_command()

    def read_config(self, config):
        super(Custom, self).read_config(config)

        self.command = config['command']

    def config(self):
        config = super(Custom, self).config()

        config['command'] = self.command

        return config

    def ask_command(self):
        return click.prompt('Enter the command you want to execute to perform backups')
