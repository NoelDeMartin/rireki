import click
import json
import os
import signal
import subprocess

from rireki.core.driver import Driver
from rireki.utils.file_helpers import file_put_contents


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
            self.__kill_process(process)
            raise Exception('Command timed out after %s seconds' % self.timeout) from e

        if process.returncode != 0:
            raise Exception(
                'Command failed with return code %s\n\nstdout:\n%s\nstderr:\n%s' %
                (process.returncode, stdout, stderr)
            )

        return {
            'stdout': stdout,
            'stderr': stderr,
        }

    def __kill_process(self, process):
        if hasattr(os, 'killpg'):
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except OSError:
                pass
        else:
            process.kill()

        process.communicate()
