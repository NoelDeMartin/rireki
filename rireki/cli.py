import click

from rireki import __version__
from rireki.commands.add import add
from rireki.commands.backup import backup
from rireki.commands.clean import clean
from rireki.commands.status import status
from rireki.core.config import Config


@click.group()
@click.version_option(__version__, prog_name='rireki')
def cli():
    Config.load()


cli.add_command(add)
cli.add_command(backup)
cli.add_command(clean)
cli.add_command(status)

if __name__ == '__main__':
    cli()
