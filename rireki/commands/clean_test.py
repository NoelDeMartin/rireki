import os

from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch
from rireki.utils.time_helpers import now, DAY_SECONDS, YEAR_SECONDS


class TestBackup(TestCase):

    def test_without_installed_projects(self):
        # Execute
        result = Cli.run('clean')

        # Assert
        assert result.exit_code == 0
        assert 'No projects installed!' in result.output

    def test_without_stale_backups(self):
        # Prepare
        project = self._create_project(
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
        )

        # Execute
        result = Cli.run('clean')

        # Assert
        assert result.exit_code == 0
        assert ('Project "%s" does not have any stale backups' % project.name) in result.output
        assert 'Done' in result.output
        assert 'Error' not in result.output

    def test_with_stale_directory_backups(self):
        # Prepare
        project = self._create_project(
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
            retention={'last_backups_retention': 1, 'year_backups_retention': 'monthly'}
        )

        today = now()
        yesterday = today - DAY_SECONDS
        last_month = today - YEAR_SECONDS

        touch('/tmp/rireki_testing/store/%s' % today)
        touch('/tmp/rireki_testing/store/%s' % yesterday)
        touch('/tmp/rireki_testing/store/%s' % last_month)

        # Execute
        result = Cli.run('clean')

        # Assert
        assert result.exit_code == 0
        assert ('Cleaning up %s...' % project.name) in result.output
        assert str(yesterday) in result.output
        assert 'Done' in result.output
        assert 'Error' not in result.output

        assert os.path.exists('/tmp/rireki_testing/store/%s' % today)
        assert not os.path.exists('/tmp/rireki_testing/store/%s' % yesterday)
        assert os.path.exists('/tmp/rireki_testing/store/%s' % last_month)

    def test_with_stale_file_backups(self):
        # Prepare
        project = self._create_project(
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
            driver='files',
            retention={'last_backups_retention': 1, 'year_backups_retention': 'monthly'},
        )

        today = now()
        yesterday = today - DAY_SECONDS
        last_month = today - YEAR_SECONDS

        touch('/tmp/rireki_testing/store/%s.zip' % today)
        touch('/tmp/rireki_testing/store/%s.zip' % yesterday)
        touch('/tmp/rireki_testing/store/%s.zip' % last_month)

        # Execute
        result = Cli.run('clean')

        # Assert
        assert result.exit_code == 0
        assert ('Cleaning up %s...' % project.name) in result.output
        assert str(yesterday) in result.output
        assert 'Done' in result.output
        assert 'Error' not in result.output

        assert os.path.exists('/tmp/rireki_testing/store/%s.zip' % today)
        assert not os.path.exists('/tmp/rireki_testing/store/%s.zip' % yesterday)
        assert os.path.exists('/tmp/rireki_testing/store/%s.zip' % last_month)
