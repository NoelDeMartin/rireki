import click

from rireki.commands.add import add
from rireki.commands.backup import backup
from rireki.commands.status import status
from rireki.core.config import Config


@click.group()
def cli():
    Config.load()


cli.add_command(add)
cli.add_command(backup)
cli.add_command(status)

if __name__ == '__main__':
    cli()
