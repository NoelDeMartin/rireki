from mock import Mock
from rireki.core.project import Project
from rireki.drivers.custom import Custom
from rireki.testing.test_case import TestCase


class TestCustom(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self.driver = Custom()
        self.driver.project = Project(self.faker.name(), Mock(), Mock())

    # Golden path tested at rireki/commands/backup_test.py

    def test_timeout(self):
        # Prepare
        self.driver.load_config({
            'frequency': 42,
            'command': 'while true; do echo; done',
            'timeout': 0,
        })

        # Execute
        with self.assertRaises(Exception):
            self.driver.perform_backup()

        # Assert
        self.driver.project.store.create_backup.assert_not_called()

    def test_error(self):
        # Prepare
        self.driver.load_config({
            'frequency': 42,
            'command': 'exit 1',
            'timeout': 60,
        })

        # Execute
        with self.assertRaises(Exception):
            self.driver.perform_backup()

        # Assert
        self.driver.project.store.create_backup.assert_not_called()
