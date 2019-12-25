import os
import re

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch
from rireki.utils.time_helpers import now


class TestStatus(TestCase):

    def test_without_installed_projects(self):
        # Execute
        result = Cli.run('status')

        # Assert
        assert result.exit_code == 0
        assert 'No projects installed!' in result.output

        assert not os.path.exists(self.home_path)

    def test_with_one_project_with_backups_pending(self):
        # Prepare
        project = self._create_project(driver='files', store='local')

        # Execute
        result = Cli.run('status')

        # Assert
        assert result.exit_code == 0

        output_lines = result.output.splitlines()
        assert len(output_lines) == 2
        assert project.name in output_lines[1]
        assert 'files' in output_lines[1]
        assert 'local' in output_lines[1]
        assert 'backup-pending' in output_lines[1]

    def test_with_one_project_backed_up(self):
        # Prepare
        project = self._create_project(
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
        )

        touch('/tmp/rireki_testing/store/%s/backup' % now())

        # Execute
        result = Cli.run('status')

        # Assert
        assert result.exit_code == 0

        output_lines = result.output.splitlines()
        assert len(output_lines) == 2
        assert project.name in output_lines[1]
        assert re.search('Backed up \\d seconds ago', output_lines[1])
