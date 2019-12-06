import os

from rireki.lib.config import Config
from rireki.lib.project import Project

def get_projects():
    if not os.path.exists(Config.projects_path):
        return []

    return [Project(f[:-5]) for f in os.listdir(Config.projects_path)]

def project_exists(name):
    return os.path.exists('%s/%s.conf' % (Config.projects_path, name))

def install_project(name):
    if not os.path.exists(Config.projects_path):
        os.makedirs(Config.projects_path)

    open('%s/%s.conf' % (Config.projects_path, name), 'w').close()
