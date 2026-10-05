import os


class Config:
    home_path = None
    projects_path = None

    @classmethod
    def load(cls):
        cls.home_path = os.environ.get('RIREKI_HOME') or cls._default_home()
        cls.projects_path = cls.home_path + '/projects'

    @classmethod
    def _default_home(cls):
        return os.path.expanduser('~/.rireki')
