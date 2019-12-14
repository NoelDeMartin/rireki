import os
import shutil
import toml
import unittest

from faker import Faker
from rireki.core.driver import Driver
from rireki.core.project import Project
from rireki.core.storage import Storage
from rireki.testing.cli import Cli


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

        self.home_path = '/tmp/rireki_testing'
        self.faker = Faker()

    def setUp(self):
        Cli.reset()
        Cli.set_environment_variable('RIREKI_HOME', self.home_path)

    def tearDown(self):
        if os.path.exists(self.home_path):
            shutil.rmtree(self.home_path)

    def create_project(self, name=None, driver=None, driver_config={}, storage=None, storage_config={}):
        name = name or self.faker.name()
        driver_config = self.create_driver_config(driver, driver_config)
        storage_config = self.create_storage_config(storage, storage_config)

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
            self.create_driver(driver, driver_config),
            self.create_storage(storage, storage_config),
        )

    def create_driver(self, name, config):
        driver = Driver(name)

        driver.read_config(config)

        return driver

    def create_driver_config(self, name=None, config={}):
        name = name or 'custom'
        config['name'] = name
        config['frequency'] = config.get('frequency') or 42

        if name == 'zip':
            config['path'] = config.get('path') or '/tmp'
        elif name == 'custom':
            config['command'] = config.get('command') or ''

        return config

    def create_storage(self, name, config):
        storage = Storage(name)

        storage.read_config(config)

        return storage

    def create_storage_config(self, name=None, config={}):
        name = name or 'local'
        config['name'] = name

        if name == 'local':
            config['path'] = config.get('path') or '/tmp'

        return config
