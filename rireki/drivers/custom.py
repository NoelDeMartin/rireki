import json
import os
import shutil
import subprocess

from rireki.core.driver import Driver
from rireki.core.traits.has_command import HasCommand
from rireki.utils.file_helpers import file_put_contents
from rireki.utils.time_helpers import now


class Custom(Driver, HasCommand):
    NAME = 'custom'

    def __init__(self):
        Driver.__init__(self, self.NAME, [HasCommand])

    def _prepare_backup_files(self):
        logs = self.__run_command()
        tmp_path = '/tmp/rireki-custom-' + self.project.slug + '-' + str(now())

        file_put_contents(os.path.join(tmp_path, 'logs.json'), json.dumps(logs))

        return [os.path.join(tmp_path, 'logs.json')]

    def _clean_backup_files(self, files):
        shutil.rmtree(os.path.dirname(files[0]))

    def __run_command(self):
        process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output = str(process.stdout.read())

        return {'output': output}
