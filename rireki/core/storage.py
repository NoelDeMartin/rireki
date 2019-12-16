import re

from rireki.core.configurable import Configurable


class Storage(Configurable):

    def get_last_backup(self):
        backups = self.get_backups()

        if not backups:
            return None

        return backups[0]

    def get_backups(self):
        raise Exception('Storage %s get_backups method is not implemented' % self.name)

    def parse_timestamp(self, file_name):
        matches = re.findall('(\\d+)\\.', file_name)

        return int(matches[-1]) if matches else 0
