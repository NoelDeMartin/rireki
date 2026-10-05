import click

from rireki.core.project import Project
from rireki.core.projects_manager import ProjectsManager
from rireki.drivers.index import drivers
from rireki.stores.index import stores
from rireki.utils.log_helpers import log


@click.command()
@click.argument('name')
@click.option('--driver', type=click.Choice(drivers.keys()), help='Backups driver')
@click.option('--store', type=click.Choice(stores.keys()), help='Backups store')
def add(name, driver=None, store=None):
    """Install a new project"""

    if ProjectsManager.project_exists(name):
        raise click.ClickException(f'Project with name "{name}" already installed!')

    driver = _resolve_driver(driver)
    store = _resolve_store(store)

    _add_new_project(name, driver, store)


def _resolve_driver(driver):
    if driver:
        return driver

    return click.prompt(
        'Which driver would you like to use to backup this project?',
        type=click.Choice(drivers.keys()),
    )


def _resolve_store(store):
    if store:
        return store

    return click.prompt(
        'Which store would you like to use to persist this project?',
        type=click.Choice(stores.keys()),
    )


def _add_new_project(project_name, driver_name, store_name):
    driver = _create_driver(driver_name)
    store = _create_store(store_name)
    project = _create_project(project_name, driver, store)

    ProjectsManager.install_project(project)

    log(f'Project "{project.name}" has been installed!')


def _create_driver(name):
    driver = drivers[name]()

    driver.ask_config()

    return driver


def _create_store(name):
    store = stores[name]()

    store.ask_config()

    return store


def _create_project(name, driver, store):
    return Project(name, driver, store)
