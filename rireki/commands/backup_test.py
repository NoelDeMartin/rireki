import json
import os

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch, file_get_contents
from rireki.utils.output import format_time
from rireki.utils.time_helpers import now, set_testing_now


class TestBackup(TestCase):

    def test_without_installed_projects(self):
        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert 'No projects installed!' in result.output

    def test_without_pending_backups(self):
        # Prepare
        project = self._create_project(
            storage='local',
            storage_config={'path': '/tmp/rireki_testing/storage'},
        )

        touch('/tmp/rireki_testing/storage/%s/backup' % now())

        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert ('Project "%s" does not have any pending backups' % project.name) in result.output
        assert 'Done' in result.output

    def test_with_custom_driver(self):
        # Prepare
        time = now()
        command_output = self.faker.sentence()
        storage_path = '/tmp/rireki_testing/storage'
        project = self._create_project(
            driver='custom',
            driver_config={'command': 'echo "%s"' % command_output},
            storage='local',
            storage_config={'path': storage_path},
        )

        set_testing_now(time)

        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert ('Backing up %s...' % project.name) in result.output
        assert 'Done' in result.output

        backup_path = os.path.join(
            storage_path,
            '{}-backup-{}-{}'.format(project.slug, format_time(time), time),
            'logs.json',
        )
        assert os.path.exists(backup_path)

        logs = json.loads(file_get_contents(backup_path))
        assert command_output in logs.get('output')
