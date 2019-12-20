from rireki.core.backup import Backup
from rireki.core.traits.configurable import Configurable
from rireki.utils.array_helpers import array_map
from rireki.utils.output import format_time
from rireki.utils.time_helpers import now


class Storage(Configurable):

    def __init__(self, name, traits=[]):
        Configurable.__init__(self, name, traits)

        self.project = None

    def upload_backup_files(self, files):
        folder_name = '{slug}-backup-{date}-{timestamp}'.format(
            slug=self.project.slug,
            date=format_time(now()),
            timestamp=now(),
        )

        for file in files:
            self._upload_file(folder_name, file)

    def get_last_backup(self):
        backups = self.get_backups()

        if not backups:
            return None

        return backups[0]

    def get_backups(self):
        names = self._get_backup_names()

        return array_map(lambda name: Backup(name), names)

    def _get_backup_names(self):
        raise Exception('%s storage must implement _get_backup_names method' % self.name)

    def _upload_file(self, folder_name, files):
        raise Exception('%s storage must implement _upload_file method' % self.name)
