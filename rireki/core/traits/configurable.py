class Configurable():

    def __init__(self, name, traits=[]):
        self.name = name
        self.__traits = traits

        self.__invoke_traits('__init__')

    def ask_config(self):
        self.__invoke_traits('ask_config')

    def load_config(self, config):
        self.__invoke_traits('load_config', config)

    def get_config(self):
        config = {'name': self.name}
        trait_configs = self.__invoke_traits('get_config')

        for trait_config in trait_configs:
            config.update(trait_config)

        return config

    def __invoke_traits(self, method, *args):
        results = []

        for trait in self.__traits:
            results.append(getattr(trait, method)(self, *args))

        return results
