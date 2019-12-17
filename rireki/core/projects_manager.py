import os
import toml

from rireki.core.config import Config
from rireki.core.project import Project
from rireki.drivers.all import drivers
from rireki.storages.all import storages


def get_projects():
    if not os.path.exists(Config.projects_path):
        return []

    return [__parse_project_config(file_name[:-5]) for file_name in os.listdir(Config.projects_path)]


def get_project_by_name(name):
    if not project_exists(name):
        return None

    return __parse_project_config(name)


def project_exists(name):
    return os.path.exists('%s/%s.conf' % (Config.projects_path, name))


def install_project(project):
    if not os.path.exists(Config.projects_path):
        os.makedirs(Config.projects_path)

    with open('%s/%s.conf' % (Config.projects_path, project.name), 'w') as config_file:
        config = {'name': project.name}

        config['driver'] = project.driver.get_config()
        config['storage'] = project.storage.get_config()

        config_file.write(toml.dumps(config))


def __parse_project_config(project_name):
    config = toml.load('%s/%s.conf' % (Config.projects_path, project_name))

    name = config['name']
    driver = drivers[config['driver']['name']]()
    storage = storages[config['storage']['name']]()

    driver.load_config(config['driver'])
    storage.load_config(config['storage'])

    return Project(name, driver, storage)
