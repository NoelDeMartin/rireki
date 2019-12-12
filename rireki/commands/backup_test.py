from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase


class TestBackup(TestCase):

    def test_all(self):
        # Execute
        result = Cli.run('backup')

        # Assert
        assert result.exit_code == 0
        assert 'No projects installed!' in result.output
