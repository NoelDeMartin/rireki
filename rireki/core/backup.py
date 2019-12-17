import re


class Backup(object):

    @classmethod
    def parse_timestamp(cls, file_name):
        matches = re.findall('(\\d+)\\.', file_name)

        return int(matches[-1]) if matches else 0

    def __init__(self, time, file_name):
        self.time = time
        self.file_name = file_name
