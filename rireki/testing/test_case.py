import os
import shutil
import toml
import unittest

from faker import Faker
from rireki.core.project import Project
from rireki.drivers.index import drivers
from rireki.stores.index import stores
from rireki.testing.cli import Cli


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        self.home_path = '/tmp/rireki_testing'
        self.faker = Faker()

    def setUp(self):
        Cli.reset()
        Cli.set_environment_variable('RIREKI_HOME', self.home_path)

        if os.path.exists(self.home_path):
            shutil.rmtree(self.home_path)

    def _create_project(self, name=None, retention={}, driver=None, driver_config={}, store=None, store_config={}):
        name = name or self.faker.name()
        driver_config = self.__create_driver_config(driver, driver_config)
        store_config = self.__create_store_config(store, store_config)

        if not os.path.exists('%s/projects' % self.home_path):
            os.makedirs('%s/projects' % self.home_path)

        with open('%s/projects/%s.conf' % (self.home_path, name), 'w') as config_file:
            config = {
                'name': name,
                'driver': driver_config,
                'store': store_config,
            }

            if 'last_backups_retention' in retention:
                config['last_backups_retention'] = retention['last_backups_retention']

            if 'year_backups_retention' in retention:
                config['year_backups_retention'] = retention['year_backups_retention']

            if 'ancient_backups_retention' in retention:
                config['ancient_backups_retention'] = retention['ancient_backups_retention']

            config_file.write(toml.dumps(config))

        return Project(
            name,
            self.__create_driver(driver_config),
            self.__create_store(store_config),
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
            config['paths'] = config.get('paths') or ['/tmp/rireki_testing/project']
        elif name == 'custom':
            config['command'] = config.get('command') or ''
            config['timeout'] = config.get('timeout') or 60

        return config

    def __create_store(self, config):
        store = stores[config['name']]()

        store.load_config(config)

        return store

    def __create_store_config(self, name=None, config={}):
        name = name or 'local'
        config['name'] = name

        if name == 'local':
            config['path'] = config.get('path') or '/tmp/rireki_testing/store'

        return config
