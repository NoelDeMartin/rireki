import os

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase


class TestStatus(TestCase):

    def test_without_installed_projects(self):
        # Execute
        result = Cli.run('status')

        # Assert
        assert result.exit_code == 0
        assert 'No projects installed!' in result.output

        assert not os.path.exists(self.home_path)

    def test_with_one_project_installed(self):
        # Prepare
        project = self.create_project(driver='zip')

        # Execute
        result = Cli.run('status')

        # Assert
        assert result.exit_code == 0

        output_lines = result.output.splitlines()
        assert len(output_lines) == 2
        assert project.name in output_lines[1]
        assert 'zip' in output_lines[1]
        assert 'backup-pending' in output_lines[1]
