class Configurable():

    def __init__(self, name=None):
        self.name = name or self.NAME

    def ask_config(self):
        pass

    def load_config(self, config):
        pass

    def get_config(self):
        return {'name': self.name}
