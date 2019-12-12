import os
import shutil
import toml
import unittest

from faker import Faker
from rireki.lib.project import Project
from rireki.testing.cli import Cli


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

        self.home_path = '/tmp/rireki_testing'
        self.fake = Faker()

    def setUp(self):
        Cli.reset()
        Cli.set_environment_variable('RIREKI_HOME', self.home_path)

    def tearDown(self):
        if os.path.exists(self.home_path):
            shutil.rmtree(self.home_path)

    def create_project(self, name=None, driver=None):
        name = name or self.fake.name()
        driver_config = self.create_driver_config(driver)

        if not os.path.exists('%s/projects' % self.home_path):
            os.makedirs('%s/projects' % self.home_path)

        with open('%s/projects/%s.conf' % (self.home_path, name), 'w') as config_file:
            config = {
                'name': name,
                'driver': driver_config,
            }

            config_file.write(toml.dumps(config))

        return Project(name, driver)

    def create_driver_config(self, driver=None):
        driver = driver or 'zip'
        config = {
            'name': driver,
            'frequency': 42,
        }

        if driver == 'zip':
            config['path'] = '/tmp'
        elif driver == 'custom':
            config['command'] = '-'

        return config
