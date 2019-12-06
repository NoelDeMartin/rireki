from click.testing import CliRunner

from rireki.main import cli

class Cli():
    runner = CliRunner()
    env = {}

    @classmethod
    def reset(cls):
        cls.runner = CliRunner()
        cls.env = {}

    @classmethod
    def set_environment_variable(cls, name, value):
        cls.env[name] = value

    @classmethod
    def run(cls, *args):
        return cls.runner.invoke(cli, args, env=cls.env)
