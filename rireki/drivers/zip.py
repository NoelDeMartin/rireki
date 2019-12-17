from rireki.core.driver import Driver
from rireki.core.traits.has_path import HasPath


class Zip(Driver, HasPath):
    NAME = 'zip'

    def __init__(self):
        Driver.__init__(self, self.NAME, [HasPath])
