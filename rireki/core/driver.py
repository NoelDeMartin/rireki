import os
import shutil

from rireki.core.traits.configurable import Configurable
from rireki.core.traits.has_frequency import HasFrequency
from rireki.utils.time_helpers import now


class Driver(Configurable, HasFrequency):

    def __init__(self, name, traits=[]):
        Configurable.__init__(self, name, [HasFrequency] + traits)

        self.project = None

    def has_pending_backups(self, last_backup_time):
        frequency_in_seconds = self.frequency * 60

        return last_backup_time < now() - frequency_in_seconds

    def perform_backup(self):
        tmp_path = self._create_temporary_folder()

        try:
            self._prepare_backup_files(tmp_path)
            self.project.storage.upload_backup_files(tmp_path)
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
