import os

from rireki.core.backup import Backup
from rireki.core.configurable import Configurable
from rireki.utils.file_helpers import file_get_extension
from rireki.utils.output import format_time
from rireki.utils.time_helpers import now


class Store(Configurable):

    def __init__(self):
        Configurable.__init__(self)

        self.project = None

    def create_backup(self, files_path):
        backup_name = '{slug}-backup-{date}-{timestamp}'.format(
            slug=self.project.slug,
            date=format_time(now(), 'date'),
            timestamp=now(),
        )

        if os.path.isfile(files_path):
            self._upload_file(
                files_path,
                '{}.{}'.format(backup_name, file_get_extension(files_path)),
            )
        elif os.path.isdir(files_path):
            for file in os.listdir(files_path):
                self._upload_file(
                    os.path.join(files_path, file),
                    os.path.join(backup_name, file),
                )

    def get_last_backup(self):
        backups = self.get_backups()

        if not backups:
            return None

        return backups[0]

    def get_backups(self):
        names = self._get_backup_names()

        return [Backup(name) for name in names if Backup.is_backup_name(name)]

    def _get_backup_names(self):
        raise Exception('%s store must implement _get_backup_names method' % self.name)

    def _upload_file(self, source, destination):
        raise Exception('%s store must implement _upload_file method' % self.name)
