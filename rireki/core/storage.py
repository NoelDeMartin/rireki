class Storage(object):

    def __init__(self, name):
        self.name = name

    def ask_config(self):
        pass

    def read_config(self, config):
        pass

    def config(self):
        return {
            'name': self.name,
        }
