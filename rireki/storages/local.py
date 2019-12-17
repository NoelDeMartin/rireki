import os

from rireki.core.backup import Backup
from rireki.core.storage import Storage
from rireki.core.traits.has_path import HasPath


class Local(Storage, HasPath):
    NAME = 'local'

    def __init__(self):
        Storage.__init__(self, self.NAME, [HasPath])

    def get_backups(self):
        backups = []

        if not os.path.exists(self.path):
            return backups

        for file_name in os.listdir(self.path):
            time = Backup.parse_timestamp(file_name)

            backups.append(Backup(time, file_name))

        return backups
