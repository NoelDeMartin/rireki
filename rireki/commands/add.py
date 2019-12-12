import click

from rireki.lib.projects_manager import project_exists, install_project
from rireki.drivers.all import drivers
from rireki.lib.project import Project


@click.command()
@click.argument('name')
@click.option('--driver', type=click.Choice(drivers.keys()), help='Backups driver')
def add(name, driver=None):
    """Install a new project"""

    if project_exists(name):
        click.echo('Project with name "%s" already installed!' % name)
        return

    if not driver:
        driver = click.prompt(
            'Which driver would you like to use to backup this project?',
            type=click.Choice(drivers.keys()),
        )

    add_new_project(name, driver)


def add_new_project(project_name, driver_name):
    driver = create_driver(driver_name)
    project = create_project(project_name, driver)

    click.echo('Installing "%s" project...' % project.name)

    install_project(project)

    click.echo('Done!')


def create_driver(name):
    driver = drivers[name]()

    driver.ask_config()

    return driver


def create_project(name, driver):
    return Project(name, driver)
