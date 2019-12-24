import os

from rireki.core.backup import Backup
from rireki.core.configurable import Configurable
from rireki.utils.output import format_time
from rireki.utils.time_helpers import now


class Storage(Configurable):

    def __init__(self):
        Configurable.__init__(self)

        self.project = None

    def upload_backup_files(self, path):
        folder_name = '{slug}-backup-{date}-{timestamp}'.format(
            slug=self.project.slug,
            date=format_time(now(), 'date'),
            timestamp=now(),
        )

        for file in os.listdir(path):
            self._upload_file(folder_name, os.path.join(path, file))

    def get_last_backup(self):
        backups = self.get_backups()

        if not backups:
            return None

        return backups[0]

    def get_backups(self):
        names = self._get_backup_names()

        return [Backup(name) for name in names if Backup.is_backup_name(name)]

    def _get_backup_names(self):
        raise Exception('%s storage must implement _get_backup_names method' % self.name)

    def _upload_file(self, folder_name, files):
        raise Exception('%s storage must implement _upload_file method' % self.name)
