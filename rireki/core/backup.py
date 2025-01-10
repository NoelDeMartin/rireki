import re
from datetime import datetime

from rireki.utils.time_helpers import now
from rireki.core.retention_policy import RetentionPolicy


class Backup(object):

    @classmethod
    def is_backup_name(cls, name):
        return re.search('(\\d+)$', name)

    def __init__(self, name):
        self.name = name

    @property
    def time(self):
        matches = re.findall('(\\d+)$', self.name)

        return int(matches[-1]) if matches else 0

    def get_age(self):
        return now() - self.time

    def retain(self, previous_backup, retention_policy):
        if retention_policy == RetentionPolicy.NONE:
            return False

        if not previous_backup:
            return True

        backup_date = datetime.fromtimestamp(self.time)
        previous_date = datetime.fromtimestamp(previous_backup.time)

        if retention_policy == RetentionPolicy.YEARLY:
            return backup_date.year != previous_date.year

        if retention_policy == RetentionPolicy.MONTHLY:
            return (backup_date.year, backup_date.month) != (previous_date.year, previous_date.month)

        if retention_policy == RetentionPolicy.WEEKLY:
            backup_year, backup_week = backup_date.isocalendar()[:2]
            previous_year, previous_week = previous_date.isocalendar()[:2]
            return (backup_year, backup_week) != (previous_year, previous_week)

        return True
