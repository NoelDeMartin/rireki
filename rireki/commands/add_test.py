import os
import toml

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase
from rireki.utils.string_helpers import str_slug


class TestAdd(TestCase):

    def test_existing_project(self):
        # Prepare
        project = self._create_project()

        # Execute
        result = Cli.run('add', project.name)

        # Assert
        assert result.exit_code == 0
        assert ('Project with name "%s" already installed!' % project.name) in result.output

    def test_new_project(self):
        # Prepare
        project_name = self.faker.name()

        # Execute
        result = Cli.run(
            'add', project_name,
            '--driver=custom',
            '--store=local',
            input=('daily', '-', '/tmp'),
        )

        # Assert
        assert result.exit_code == 0
        assert ('Project "%s" has been installed!' % project_name) in result.output

        assert os.path.exists('%s/projects/%s.conf' % (self.home_path, project_name))

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'name' in config
        assert config['name'] == project_name

    def test_new_project_with_files_driver(self):
        # Prepare
        project_name = self.faker.name()
        driver_name = 'files'
        driver_frequency_name = 'daily'
        driver_frequency_minutes = 1440
        driver_paths = [
            '/tmp',
            os.path.join('tmp', str_slug(self.faker.word())),
        ]

        # Execute
        result = Cli.run(
            'add', project_name,
            '--driver=' + driver_name,
            '--store=local',
            input=self.__get_new_project_with_files_driver_input(
                driver_frequency_name,
                driver_paths,
            ),
        )

        # Assert
        assert result.exit_code == 0

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'driver' in config
        assert config['driver']['name'] == driver_name
        assert config['driver']['frequency'] == driver_frequency_minutes
        assert config['driver']['paths'] == driver_paths

    def test_new_project_with_custom_driver(self):
        # Prepare
        project_name = self.faker.name()
        driver_name = 'custom'
        driver_frequency_name = 'custom'
        driver_frequency_minutes = 42
        driver_command = self.faker.word()

        # Execute
        result = Cli.run(
            'add', project_name,
            '--driver=' + driver_name,
            '--store=local',
            input=(driver_frequency_name, str(driver_frequency_minutes), driver_command, '/tmp'),
        )

        # Assert
        assert result.exit_code == 0

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'driver' in config
        assert config['driver']['name'] == driver_name
        assert config['driver']['frequency'] == driver_frequency_minutes
        assert config['driver']['command'] == driver_command

    def test_new_project_with_local_store(self):
        # Prepare
        project_name = self.faker.name()
        store_name = 'local'
        store_path = '/tmp'

        # Execute
        result = Cli.run(
            'add', project_name,
            '--driver=custom',
            '--store=' + store_name,
            input=('daily', '-', store_path),
        )

        # Assert
        assert result.exit_code == 0

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'store' in config
        assert config['store']['name'] == store_name
        assert config['store']['path'] == store_path

    def __get_new_project_with_files_driver_input(self, driver_frequency_name, driver_paths):
        input = []

        # Driver frequency
        input.append(driver_frequency_name)

        # Driver paths - First path
        input.append(driver_paths[0])
        # Driver paths - Yes, add more paths
        input.append('y')
        # Driver paths - Second path
        input.append(driver_paths[1])
        # Driver paths - Yes, path is correct even though it doesn't exist
        input.append('y')
        # Driver paths - No, no more paths
        input.append('N')

        # store path
        input.append('/tmp')

        return input
