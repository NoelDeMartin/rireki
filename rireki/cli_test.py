from rireki import __version__
from rireki.testing.cli import Cli
from rireki.testing.test_case import TestCase


class TestCli(TestCase):

    def test_version(self):
        # Execute
        result = Cli.run('--version')

        # Assert
        assert result.exit_code == 0
        assert ('rireki, version %s' % __version__) in result.output
