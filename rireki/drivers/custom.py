import json
import os
import signal
import subprocess

import click

from rireki.core.driver import Driver
from rireki.core.errors import BackupError
from rireki.utils.file_helpers import file_put_contents


class Custom(Driver):
    NAME = 'custom'

    def __init__(self):
        Driver.__init__(self)

        self.command = None
        self.timeout = 60

    def ask_config(self):
        Driver.ask_config(self)

        self.command = self._ask_command()

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
        logs = self._run_command(path)

        file_put_contents(os.path.join(path, 'logs.json'), json.dumps(logs))

        return path

    def _ask_command(self):
        return click.prompt('Enter the command you want to execute to perform backups')

    def _run_command(self, path):
        process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors='replace',
            start_new_session=True,
            env={**os.environ, 'RIREKI_BACKUP_PATH': path},
        )

        try:
            stdout, stderr = process.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired as e:
            self._kill_process(process)
            raise BackupError(f'Command timed out after {self.timeout} seconds') from e

        if process.returncode != 0:
            raise BackupError(
                f'Command failed with return code {process.returncode}\n\nstdout:\n{stdout}\nstderr:\n{stderr}'
            )

        return {
            'stdout': stdout,
            'stderr': stderr,
        }

    def _kill_process(self, process):
        if hasattr(os, 'killpg'):
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except OSError:
                pass
        else:
            process.kill()

        process.communicate()
