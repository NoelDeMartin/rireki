from rireki.core.configurable import Configurable


class Storage(Configurable):

    def get_last_backup(self):
        backups = self.get_backups()

        if not backups:
            return None

        return backups[0]

    def get_backups(self):
        raise Exception('Storage %s does not support get_backups method' % self.name)
