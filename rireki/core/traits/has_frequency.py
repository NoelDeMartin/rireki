import click

from rireki.utils.string_helpers import str_studly

DEFAULT_FREQUENCIES = {
    'Hourly': 60,
    'Daily': 1440,
    'Weekly': 10080,
    'Monthly': 43200,
    'Custom': None,
}


class HasFrequency():

    def __init__(self):
        self.frequency = None

    def ask_config(self):
        self.frequency = self.__ask_frequency()

    def load_config(self, config):
        self.frequency = config['frequency']

    def get_config(self):
        return {'frequency': self.frequency}

    def __ask_frequency(self):
        frequency = click.prompt(
            'How often should the backups be performed?',
            type=click.Choice(DEFAULT_FREQUENCIES.keys(), case_sensitive=False),
        )

        frequency = DEFAULT_FREQUENCIES[str_studly(frequency)]

        if not frequency:
            frequency = self.__ask_custom_frequency()

        return frequency

    def __ask_custom_frequency(self):
        return click.prompt(
            'Enter your custom frequency (in minutes)',
            type=click.IntRange(min=1)
        )
