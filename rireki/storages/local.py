import os

from rireki.core.storage import Storage
from rireki.core.traits.has_path import HasPath
from shutil import copyfile


class Local(Storage, HasPath):
    NAME = 'local'

    def __init__(self):
        Storage.__init__(self, self.NAME, [HasPath])

    def _get_backup_names(self):
        if not os.path.exists(self.path):
            return []

        return os.listdir(self.path)

    def _upload_file(self, folder_name, file):
        root_path = os.path.join(self.path, folder_name)

        if not os.path.exists(root_path):
            os.makedirs(root_path)

        copyfile(file, os.path.join(root_path, os.path.basename(file)))
