import click

from rireki.utils.string_helpers import str_studly


DEFAULT_FREQUENCIES = {
    'Hourly': 60,
    'Daily': 1440,
    'Weekly': 10080,
    'Monthly': 43200,
    'Custom': None,
}


class Driver(object):

    def __init__(self, name):
        self.name = name
        self.frequency = None

    def ask_config(self):
        self.frequency = self.ask_frequency()

    def read_config(self, config):
        self.frequency = config['frequency']

    def config(self):
        return {
            'name': self.name,
            'frequency': self.frequency,
        }

    def ask_frequency(self):
        frequency = click.prompt(
            'How often should the backups be performed?',
            type=click.Choice(DEFAULT_FREQUENCIES.keys(), case_sensitive=False),
        )

        frequency = DEFAULT_FREQUENCIES[str_studly(frequency)]

        if not frequency:
            frequency = self.ask_custom_frequency()

        return frequency

    def ask_custom_frequency(self):
        return click.prompt(
            'Enter your custom frequency (in minutes)',
            type=click.IntRange(min=1)
        )
