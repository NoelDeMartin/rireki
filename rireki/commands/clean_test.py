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

    def test_with_stale_backups(self):
        # Prepare
        project = self._create_project(
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
            retention={'last_backups_retention': 1, 'year_backups_retention': 'monthly'}
        )

        today = now()
        yesterday = today - DAY_SECONDS
        last_month = today - YEAR_SECONDS

        touch('/tmp/rireki_testing/store/%s/backup' % today)
        touch('/tmp/rireki_testing/store/%s/backup' % yesterday)
        touch('/tmp/rireki_testing/store/%s/backup' % last_month)

        # Execute
        result = Cli.run('clean')

        # Assert
        assert result.exit_code == 0
        assert ('Cleaning up %s...' % project.name) in result.output
        assert str(yesterday) in result.output
        assert 'Done' in result.output
        assert 'Error' not in result.output

        assert os.path.exists('/tmp/rireki_testing/store/%s/backup' % today)
        assert not os.path.exists('/tmp/rireki_testing/store/%s/backup' % yesterday)
        assert os.path.exists('/tmp/rireki_testing/store/%s/backup' % last_month)
