import json
import os
from datetime import datetime

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import file_get_contents, touch
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
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
        )

        touch(f'/tmp/rireki_testing/store/{now()}/backup')

        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert f'Project "{project.name}" does not have any pending backups' in result.output
        assert 'Done' in result.output
        assert 'Error' not in result.output

    def test_with_custom_driver(self):
        # Prepare
        time = now()
        command_output = self.faker.sentence()
        store_path = '/tmp/rireki_testing/store'
        project = self._create_project(
            driver='custom',
            driver_config={'command': f'echo "{command_output}"'},
            store='local',
            store_config={'path': store_path},
        )

        set_testing_now(time)

        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert f'Backing up {project.name}...' in result.output
        assert 'Done' in result.output
        assert 'Error' not in result.output

        backup_path = os.path.join(
            store_path,
            f"{project.slug}-backup-{format_time(time, 'date')}-{time}",
            'logs.json',
        )
        assert os.path.exists(backup_path)

        logs = json.loads(file_get_contents(backup_path))
        assert command_output in logs.get('stdout')

    def test_showing_timestamps(self):
        # Prepare
        time = now()
        command_output = self.faker.sentence()
        store_path = '/tmp/rireki_testing/store'
        project = self._create_project(
            driver='custom',
            driver_config={'command': f'echo "{command_output}"'},
            store='local',
            store_config={'path': store_path},
        )

        set_testing_now(time)

        # Execute
        result = Cli.run('backup', '--timestamps')

        # Assert
        assert result.exit_code == 0
        assert f'[{datetime.fromtimestamp(time).isoformat()}] Backing up {project.name}...' in result.output
        assert 'Done' in result.output
        assert 'Error' not in result.output

    def test_backup_failure_exits_with_error_code(self):
        # Prepare
        self._create_project(
            driver='custom',
            driver_config={'command': 'exit 1'},
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
        )

        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 1
        assert 'Error:' in result.output
        assert 'Done' not in result.output

    def test_backup_uninstalled_project_exits_with_error_code(self):
        # Execute
        result = Cli.run('backup', 'non_existent_project')

        # Assert
        assert result.exit_code == 1
        assert 'Project with name "non_existent_project" is not installed!' in result.output
