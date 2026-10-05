import os

import toml

from rireki.core.config import Config
from rireki.core.project import Project
from rireki.drivers.index import drivers
from rireki.stores.index import stores


class ProjectsManager:

    @classmethod
    def get_projects(cls):
        cls._ensure_config()

        if not os.path.exists(Config.projects_path):
            return []

        projects = []
        for file_name in os.listdir(Config.projects_path):
            file_path = os.path.join(Config.projects_path, file_name)
            if file_name.endswith('.conf') and os.path.isfile(file_path):
                projects.append(cls._parse_project_config(file_name[:-5]))

        return projects

    @classmethod
    def get_project_by_name(cls, name):
        cls._ensure_config()

        if not cls.project_exists(name):
            return None

        return cls._parse_project_config(name)

    @classmethod
    def project_exists(cls, name):
        cls._ensure_config()

        return os.path.isfile(os.path.join(Config.projects_path, f'{name}.conf'))

    @classmethod
    def install_project(cls, project):
        cls._ensure_config()

        if not os.path.exists(Config.projects_path):
            os.makedirs(Config.projects_path)

        with open(os.path.join(Config.projects_path, f'{project.name}.conf'), 'w') as config_file:
            config_file.write(toml.dumps(project.get_config()))

    @classmethod
    def _ensure_config(cls):
        if Config.projects_path is None:
            Config.load()

    @classmethod
    def _parse_project_config(cls, project_name):
        config = toml.load(os.path.join(Config.projects_path, f'{project_name}.conf'))

        driver = drivers[config['driver']['name']]()
        store = stores[config['store']['name']]()
        project = Project(config['name'], driver, store)

        project.load_config(config)

        return project
