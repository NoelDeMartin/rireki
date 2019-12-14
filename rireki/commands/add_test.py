import os
import toml

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase


class TestAdd(TestCase):

    def test_existing_project(self):
        # Prepare
        project = self.create_project()

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
            '--storage=local',
            input=('daily', '-', '/tmp'),
        )

        # Assert
        assert result.exit_code == 0
        assert ('Project "%s" has been installed!' % project_name) in result.output

        assert os.path.exists('%s/projects/%s.conf' % (self.home_path, project_name))

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'name' in config
        assert config['name'] == project_name

    def test_new_project_with_zip_driver(self):
        # Prepare
        project_name = self.faker.name()
        driver_name = 'zip'
        driver_frequency_name = 'daily'
        driver_frequency_minutes = 1440
        driver_path = '/tmp'

        # Execute
        result = Cli.run(
            'add', project_name,
            '--driver=' + driver_name,
            '--storage=local',
            input=(driver_frequency_name, driver_path, '/tmp'),
        )

        # Assert
        assert result.exit_code == 0

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'driver' in config
        assert config['driver']['name'] == driver_name
        assert config['driver']['frequency'] == driver_frequency_minutes
        assert config['driver']['path'] == driver_path

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
            '--storage=local',
            input=(driver_frequency_name, str(driver_frequency_minutes), driver_command, '/tmp'),
        )

        # Assert
        assert result.exit_code == 0

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'driver' in config
        assert config['driver']['name'] == driver_name
        assert config['driver']['frequency'] == driver_frequency_minutes
        assert config['driver']['command'] == driver_command

    def test_new_project_with_local_storage(self):
        # Prepare
        project_name = self.faker.name()
        storage_name = 'local'
        storage_path = '/tmp'

        # Execute
        result = Cli.run(
            'add', project_name,
            '--driver=custom',
            '--storage=' + storage_name,
            input=('daily', '-', storage_path),
        )

        # Assert
        assert result.exit_code == 0

        config = toml.load('%s/projects/%s.conf' % (self.home_path, project_name))

        assert 'storage' in config
        assert config['storage']['name'] == storage_name
        assert config['storage']['path'] == storage_path
