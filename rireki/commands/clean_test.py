import os
from unittest.mock import patch

from rireki.core.project import Project
from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch
from rireki.utils.time_helpers import now, set_testing_now, DAY_SECONDS, YEAR_SECONDS


class TestClean(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        set_testing_now(1750000000)

    def tearDown(self):
        TestCase.tearDown(self)

        set_testing_now(None)

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
        last_month = today - 30 * DAY_SECONDS
        last_year = today - YEAR_SECONDS

        touch('/tmp/rireki_testing/store/%s' % today)
        touch('/tmp/rireki_testing/store/%s' % yesterday)
        touch('/tmp/rireki_testing/store/%s' % last_month)
        touch('/tmp/rireki_testing/store/%s' % last_year)

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
        assert os.path.exists('/tmp/rireki_testing/store/%s' % last_year)

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
        last_month = today - 30 * DAY_SECONDS
        last_year = today - YEAR_SECONDS

        touch('/tmp/rireki_testing/store/%s.zip' % today)
        touch('/tmp/rireki_testing/store/%s.zip' % yesterday)
        touch('/tmp/rireki_testing/store/%s.zip' % last_month)
        touch('/tmp/rireki_testing/store/%s.zip' % last_year)

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
        assert os.path.exists('/tmp/rireki_testing/store/%s.zip' % last_year)

    def test_clean_failure_exits_with_error_code(self):
        # Prepare
        self._create_project(
            store='local',
            store_config={'path': '/tmp/rireki_testing/store'},
            retention={'last_backups_retention': 1, 'year_backups_retention': 'monthly'},
        )

        today = now()
        yesterday = today - DAY_SECONDS
        touch('/tmp/rireki_testing/store/%s' % today)
        touch('/tmp/rireki_testing/store/%s' % yesterday)

        with patch.object(Project, 'remove_backup', side_effect=Exception('Permission denied')):
            # Execute
            result = Cli.run('clean')

        # Assert
        assert result.exit_code == 1
        assert 'Error: Permission denied' in result.output
        assert 'Done' not in result.output

    def test_clean_uninstalled_project_exits_with_error_code(self):
        # Execute
        result = Cli.run('clean', 'non_existent_project')

        # Assert
        assert result.exit_code == 1
        assert 'Project with name "non_existent_project" is not installed!' in result.output
