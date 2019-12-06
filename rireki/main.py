import click

from rireki.lib.config import Config

@click.group()
def cli():
    Config.load()

from rireki.commands.add import add
from rireki.commands.status import status

if __name__ == '__main__':
   cli()
