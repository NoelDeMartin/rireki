from click.testing import CliRunner

from rireki.cli import cli


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
    def run(cls, *args, **kwargs):
        if 'input' in kwargs:
            input_argument = kwargs['input']

            if type(kwargs['input']) in (tuple, list):
                input = '\n'.join(input_argument)
            else:
                input = input_argument
        else:
            input = ''

        return cls.runner.invoke(cli, args, env=cls.env, input=input)
