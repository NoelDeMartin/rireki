import re


class Backup(object):

    def __init__(self, name):
        self.name = name

    @property
    def time(self):
        matches = re.findall('(\\d+)$', self.name)

        return int(matches[-1]) if matches else 0
