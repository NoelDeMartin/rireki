import os
import toml

from rireki.core.config import Config
from rireki.core.project import Project
from rireki.drivers.index import drivers
from rireki.stores.index import stores


class ProjectsManager():

    @classmethod
    def get_projects(cls):
        if not os.path.exists(Config.projects_path):
            return []

        return [cls.__parse_project_config(file_name[:-5]) for file_name in os.listdir(Config.projects_path)]

    @classmethod
    def get_project_by_name(cls, name):
        if not cls.project_exists(name):
            return None

        return cls.__parse_project_config(name)

    @classmethod
    def project_exists(cls, name):
        return os.path.exists('%s/%s.conf' % (Config.projects_path, name))

    @classmethod
    def install_project(cls, project):
        if not os.path.exists(Config.projects_path):
            os.makedirs(Config.projects_path)

        with open('%s/%s.conf' % (Config.projects_path, project.name), 'w') as config_file:
            config = {'name': project.name}

            config['driver'] = project.driver.get_config()
            config['store'] = project.store.get_config()

            config_file.write(toml.dumps(config))

    @classmethod
    def __parse_project_config(cls, project_name):
        config = toml.load('%s/%s.conf' % (Config.projects_path, project_name))

        name = config['name']
        driver = drivers[config['driver']['name']]()
        store = stores[config['store']['name']]()
        project = Project(name, driver, store)

        driver.project = project
        driver.load_config(config['driver'])

        store.project = project
        store.load_config(config['store'])

        return project
