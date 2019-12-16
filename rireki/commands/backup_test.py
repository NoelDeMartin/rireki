from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch
from rireki.utils.time_helpers import now


class TestBackup(TestCase):

    def test_without_installed_projects(self):
        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert 'No projects installed!' in result.output

    def test_without_pending_backups(self):
        # Prepare
        project = self.create_project(
            storage='local',
            storage_config={'path': '/tmp/rireki_testing/storage'},
        )

        touch('/tmp/rireki_testing/storage/%s.json' % now())

        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert ('Project "%s" does not have any pending backups' % project.name) in result.output
        assert 'Done' in result.output
