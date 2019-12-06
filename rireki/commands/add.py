import click

from rireki.lib.projects_manager import project_exists, install_project
from rireki.main import cli

@cli.command()
@click.argument('name')
def add(name):
    """Install a new project"""

    if project_exists(name):
        click.echo('Project with name "%s" already installed!' % name)
        return

    add_new_project(name)

def add_new_project(name):
    click.echo('Installing "%s" project...' % name)

    install_project(name)

    click.echo('Done!')
