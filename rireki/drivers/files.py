import os
import shutil

from rireki.core.driver import Driver
from rireki.core.traits.has_path import HasPath


class Files(Driver, HasPath):
    NAME = 'files'

    def __init__(self):
        Driver.__init__(self, self.NAME, [HasPath])

    def _prepare_backup_files(self, path):
        supported_formats = [format[0] for format in shutil.get_archive_formats()]
        format = 'zip' if 'zip' in supported_formats else 'tar'

        shutil.make_archive(os.path.join(path, 'backup'), format, self.path)
