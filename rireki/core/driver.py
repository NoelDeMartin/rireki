import click
import os
import shutil

from rireki.core.configurable import Configurable
from rireki.utils.string_helpers import str_studly
from rireki.utils.time_helpers import now

DEFAULT_FREQUENCIES = {
    'Hourly': 60,
    'Daily': 1440,
    'Weekly': 10080,
    'Monthly': 43200,
    'Custom': None,
}


class Driver(Configurable):

    def __init__(self):
        Configurable.__init__(self)

        self.project = None
        self.frequency = None

    def ask_config(self):
        Configurable.ask_config(self)

        self.frequency = self.__ask_frequency()

    def load_config(self, config):
        Configurable.load_config(self, config)

        self.frequency = config['frequency']

    def get_config(self):
        config = Configurable.get_config(self)

        config['frequency'] = self.frequency

        return config

    def has_pending_backups(self, last_backup_time):
        frequency_in_seconds = self.frequency * 60

        return last_backup_time < now() - frequency_in_seconds

    def perform_backup(self):
        tmp_path = self._create_temporary_folder()

        try:
            files_path = self._prepare_backup_files(tmp_path)

            self.project.store.create_backup(files_path)
        finally:
            self._clean_backup_files(tmp_path)

    def _create_temporary_folder(self):
        path = '/tmp/rireki-{}-{}-{}'.format(self.name, self.project.slug, now())

        os.makedirs(path)

        return path

    def _clean_backup_files(self, path):
        shutil.rmtree(path)

    def _prepare_backup_files(self, path):
        raise Exception('%s driver must implement _prepare_backup_files method' % self.name)

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
