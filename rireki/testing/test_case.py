import os
import shutil
import unittest

from faker import Faker
from rireki.testing.cli import Cli


class TestCase(unittest.TestCase):
    home_path = '/tmp/rireki_testing'
    fake = Faker()

    def setUp(self):
        Cli.reset()
        Cli.set_environment_variable('RIREKI_HOME', self.home_path)

    def tearDown(self):
        if os.path.exists(self.home_path):
            shutil.rmtree(self.home_path)
