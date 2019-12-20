import os


class Config():
    home_path = None
    projects_path = None

    @classmethod
    def load(cls):
        cls.home_path = os.environ.get('RIREKI_HOME') or cls.__default_home()
        cls.projects_path = cls.home_path + '/projects'

    @classmethod
    def __default_home(cls):
        return '%s/.rireki' % os.path.expanduser('~')
