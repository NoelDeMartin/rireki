import json
import os

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
            'timeout': 1,
        })

        # Execute
        with self.assertRaises(Exception):
            self.driver.perform_backup()

        # Assert
        self.driver.project.store.create_backup.assert_not_called()

    def test_timeout_kills_child_processes(self):
        # Prepare
        self.driver.load_config({
            'frequency': 42,
            'command': 'sleep 10 & wait',
            'timeout': 1,
        })

        # Execute
        with self.assertRaises(Exception) as ctx:
            self.driver.perform_backup()

        # Assert
        self.driver.project.store.create_backup.assert_not_called()
        self.assertIn('Command timed out after 1 seconds', str(ctx.exception))

    def test_error(self):
        # Prepare
        self.driver.load_config({
            'frequency': 42,
            'command': 'exit 1',
            'timeout': 1,
        })

        # Execute
        with self.assertRaises(Exception):
            self.driver.perform_backup()

        # Assert
        self.driver.project.store.create_backup.assert_not_called()

    def test_environment_variables_and_clean_logs(self):
        # Prepare
        captured_logs = self._capture_backup_logs()
        os.environ['RIREKI_TEST_ENV'] = 'custom_val_123'

        try:
            self.driver.load_config({
                'frequency': 42,
                'command': 'echo "env=$RIREKI_TEST_ENV,path=$RIREKI_BACKUP_PATH"',
                'timeout': 5,
            })

            # Execute
            self.driver.perform_backup()

            # Assert
            self.driver.project.store.create_backup.assert_called_once()
            self.assertIn('env=custom_val_123', captured_logs.get('stdout'))
            self.assertIn('path=/tmp/rireki-custom-', captured_logs.get('stdout'))
            self.assertFalse(captured_logs.get('stdout').startswith("b'"))
        finally:
            os.environ.pop('RIREKI_TEST_ENV', None)

    def test_large_output_does_not_deadlock(self):
        # Prepare
        captured_logs = self._capture_backup_logs()

        self.driver.load_config({
            'frequency': 42,
            'command': 'python3 -c "import sys; sys.stdout.write(\'A\' * 100000); sys.stderr.write(\'B\' * 100000)"',
            'timeout': 5,
        })

        # Execute
        self.driver.perform_backup()

        # Assert
        self.driver.project.store.create_backup.assert_called_once()
        self.assertEqual(len(captured_logs.get('stdout')), 100000)
        self.assertEqual(len(captured_logs.get('stderr')), 100000)

    def _capture_backup_logs(self):
        logs = {}

        def mock_create_backup(path):
            with open(os.path.join(path, 'logs.json')) as f:
                logs.update(json.loads(f.read()))

        self.driver.project.store.create_backup.side_effect = mock_create_backup

        return logs
