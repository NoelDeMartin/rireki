import subprocess

from rireki.core.driver import Driver
from rireki.core.traits.has_command import HasCommand


class Custom(Driver, HasCommand):
    NAME = 'custom'

    def __init__(self):
        Driver.__init__(self, self.NAME, [HasCommand])
