import os

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase


class TestAdd(TestCase):

    def test_new_project(self):
        # Prepare
        project_name = self.fake.name()

        # Execute
        result = Cli.run('add', project_name)

        # Assert
        assert result.exit_code == 0
        assert ('Installing "%s" project...' % project_name) in result.output
        assert 'Done' in result.output

        assert os.path.exists('%s/projects/%s.conf' % (self.home_path, project_name))

    def test_existing_project(self):
        # Prepare
        project_name = self.fake.name()

        if not os.path.exists('%s/projects' % self.home_path):
            os.makedirs('%s/projects' % self.home_path)

        open('%s/projects/%s.conf' % (self.home_path, project_name), 'w').close()

        # Execute
        result = Cli.run('add', project_name)

        # Assert
        assert result.exit_code == 0
        assert ('Project with name "%s" already installed!' % project_name) in result.output
