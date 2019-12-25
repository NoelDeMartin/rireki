import click

from rireki.core.project import Project
from rireki.core.projects_manager import ProjectsManager
from rireki.drivers.index import drivers
from rireki.stores.index import stores


@click.command()
@click.argument('name')
@click.option('--driver', type=click.Choice(drivers.keys()), help='Backups driver')
@click.option('--store', type=click.Choice(stores.keys()), help='Backups store')
def add(name, driver=None, store=None):
    """Install a new project"""

    if ProjectsManager.project_exists(name):
        click.echo('Project with name "%s" already installed!' % name)
        return

    driver = __resolve_driver(driver)
    store = __resolve_store(store)

    __add_new_project(name, driver, store)


def __resolve_driver(driver):
    if driver:
        return driver

    return click.prompt(
        'Which driver would you like to use to backup this project?',
        type=click.Choice(drivers.keys()),
    )


def __resolve_store(store):
    if store:
        return store

    return click.prompt(
        'Which store would you like to use to persist this project?',
        type=click.Choice(stores.keys()),
    )


def __add_new_project(project_name, driver_name, store_name):
    driver = __create_driver(driver_name)
    store = __create_store(store_name)
    project = __create_project(project_name, driver, store)

    ProjectsManager.install_project(project)

    click.echo('Project "%s" has been installed!' % project.name)


def __create_driver(name):
    driver = drivers[name]()

    driver.ask_config()

    return driver


def __create_store(name):
    store = stores[name]()

    store.ask_config()

    return store


def __create_project(name, driver, store):
    return Project(name, driver, store)
