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

    def test_with_projects_installed(self):
        # Prepare
        project_name = self.fake.name()

        if not os.path.exists('%s/projects' % self.home_path):
            os.makedirs('%s/projects' % self.home_path)

        open('%s/projects/%s.conf' % (self.home_path, project_name), 'w').close()

        # Execute
        result = Cli.run('status')

        # Assert
        assert result.exit_code == 0

        output_lines = result.output.splitlines()
        assert len(output_lines) == 2
        assert project_name in output_lines[1]
        assert 'backup-pending' in output_lines[1]
