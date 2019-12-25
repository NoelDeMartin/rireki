import click
import json
import os
import subprocess

from rireki.core.driver import Driver
from rireki.utils.file_helpers import file_put_contents
from threading import Thread


class Custom(Driver):
    NAME = 'custom'

    def __init__(self):
        Driver.__init__(self)

        self.command = None
        self.timeout = 60

    def ask_config(self):
        Driver.ask_config(self)

        self.command = self.__ask_command()

    def load_config(self, config):
        Driver.load_config(self, config)

        self.command = config['command']
        self.timeout = config['timeout']

    def get_config(self):
        config = Driver.get_config(self)

        config['timeout'] = self.timeout
        config['command'] = self.command

        return config

    def _prepare_backup_files(self, path):
        logs = self.__run_command(path)

        file_put_contents(os.path.join(path, 'logs.json'), json.dumps(logs))

        return path

    def __ask_command(self):
        return click.prompt('Enter the command you want to execute to perform backups')

    def __run_command(self, path):
        self.process = None
        self.logs = {}

        def target():
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={'RIREKI_BACKUP_PATH': path}
            )

            self.logs['stdout'] = str(self.process.stdout.read())
            self.logs['stderr'] = str(self.process.stderr.read())

        thread = Thread(target=target)

        thread.start()
        thread.join(1)
        self.process.poll()

        if thread.isAlive() or self.process.returncode is None:
            self.process.terminate()
            thread.join()
            self.process.poll()

        if self.process.returncode != 0:
            raise Exception('Command failed with return code %s' % self.process.returncode)

        return self.logs
