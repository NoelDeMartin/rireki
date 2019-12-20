import os
import shutil
import toml
import unittest

from faker import Faker
from rireki.core.project import Project
from rireki.drivers.index import drivers
from rireki.storages.index import storages
from rireki.testing.cli import Cli


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        self.home_path = '/tmp/rireki_testing'
        self.faker = Faker()

    def setUp(self):
        Cli.reset()
        Cli.set_environment_variable('RIREKI_HOME', self.home_path)

    def tearDown(self):
        if os.path.exists(self.home_path):
            shutil.rmtree(self.home_path)

    def _create_project(self, name=None, driver=None, driver_config={}, storage=None, storage_config={}):
        name = name or self.faker.name()
        driver_config = self.__create_driver_config(driver, driver_config)
        storage_config = self.__create_storage_config(storage, storage_config)

        if not os.path.exists('%s/projects' % self.home_path):
            os.makedirs('%s/projects' % self.home_path)

        with open('%s/projects/%s.conf' % (self.home_path, name), 'w') as config_file:
            config = {
                'name': name,
                'driver': driver_config,
                'storage': storage_config,
            }

            config_file.write(toml.dumps(config))

        return Project(
            name,
            self.__create_driver(driver_config),
            self.__create_storage(storage_config),
        )

    def __create_driver(self, config):
        driver = drivers[config['name']]()

        driver.load_config(config)

        return driver

    def __create_driver_config(self, name=None, config={}):
        name = name or 'custom'
        config['name'] = name
        config['frequency'] = config.get('frequency') or 42

        if name == 'files':
            config['path'] = config.get('path') or '/tmp/rireki_testing/project'
        elif name == 'custom':
            config['command'] = config.get('command') or ''
            config['timeout'] = config.get('timeout') or 60

        return config

    def __create_storage(self, config):
        storage = storages[config['name']]()

        storage.load_config(config)

        return storage

    def __create_storage_config(self, name=None, config={}):
        name = name or 'local'
        config['name'] = name

        if name == 'local':
            config['path'] = config.get('path') or '/tmp/rireki_testing/storage'

        return config
