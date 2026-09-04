import os

from rireki.core.config import Config
from rireki.core.projects_manager import ProjectsManager
from rireki.testing.test_case import TestCase
from rireki.utils.file_helpers import touch


class TestProjectsManager(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        os.environ['RIREKI_HOME'] = self.home_path
        Config.load()

    def tearDown(self):
        TestCase.tearDown(self)

        if 'RIREKI_HOME' in os.environ:
            del os.environ['RIREKI_HOME']
        Config.load()

    def test_get_projects_empty(self):
        projects = ProjectsManager.get_projects()

        assert projects == []

    def test_get_projects_returns_installed_projects(self):
        project1 = self._create_project(name='proj1')
        project2 = self._create_project(name='proj2')

        projects = ProjectsManager.get_projects()
        names = [p.name for p in projects]

        assert len(projects) == 2
        assert project1.name in names
        assert project2.name in names

    def test_get_projects_filters_non_conf_files_and_directories(self):
        valid_project = self._create_project(name='valid_project')

        touch(os.path.join(Config.projects_path, '.DS_Store'))
        touch(os.path.join(Config.projects_path, 'project.conf.bak'))
        touch(os.path.join(Config.projects_path, 'readme.txt'))

        os.makedirs(os.path.join(Config.projects_path, 'some_dir'))
        os.makedirs(os.path.join(Config.projects_path, 'fake_project.conf'))

        projects = ProjectsManager.get_projects()

        assert len(projects) == 1
        assert projects[0].name == valid_project.name

    def test_project_exists(self):
        self._create_project(name='installed')

        assert ProjectsManager.project_exists('installed') is True
        assert ProjectsManager.project_exists('not_installed') is False

        os.makedirs(os.path.join(Config.projects_path, 'dir.conf'))
        assert ProjectsManager.project_exists('dir') is False

    def test_get_project_by_name(self):
        self._create_project(name='my_project')

        project = ProjectsManager.get_project_by_name('my_project')
        assert project is not None
        assert project.name == 'my_project'

        assert ProjectsManager.get_project_by_name('unknown') is None
