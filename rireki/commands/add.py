import click

from rireki.core.project import Project
from rireki.core.projects_manager import project_exists, install_project
from rireki.drivers.all import drivers
from rireki.storages.all import storages


@click.command()
@click.argument('name')
@click.option('--driver', type=click.Choice(drivers.keys()), help='Backups driver')
@click.option('--storage', type=click.Choice(storages.keys()), help='Backups storage')
def add(name, driver=None, storage=None):
    """Install a new project"""

    if project_exists(name):
        click.echo('Project with name "%s" already installed!' % name)
        return

    driver = resolve_driver(driver)
    storage = resolve_storage(storage)

    add_new_project(name, driver, storage)


def resolve_driver(driver):
    if driver:
        return driver

    return click.prompt(
        'Which driver would you like to use to backup this project?',
        type=click.Choice(drivers.keys()),
    )


def resolve_storage(storage):
    if storage:
        return storage

    return click.prompt(
        'Which storage would you like to use to persist this project?',
        type=click.Choice(storages.keys()),
    )


def add_new_project(project_name, driver_name, storage_name):
    driver = create_driver(driver_name)
    storage = create_storage(storage_name)
    project = create_project(project_name, driver, storage)

    install_project(project)

    click.echo('Project "%s" has been installed!' % project.name)


def create_driver(name):
    driver = drivers[name]()

    driver.ask_config()

    return driver


def create_storage(name):
    storage = storages[name]()

    storage.ask_config()

    return storage


def create_project(name, driver, storage):
    return Project(name, driver, storage)
