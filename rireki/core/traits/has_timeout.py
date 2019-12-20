class HasTimeout():

    def __init__(self):
        self.timeout = 60

    def ask_config(self):
        pass

    def load_config(self, config):
        self.timeout = config['timeout']

    def get_config(self):
        return {'timeout': self.timeout}
