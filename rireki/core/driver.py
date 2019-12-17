from rireki.core.configurable import Configurable
from rireki.core.traits.has_frequency import HasFrequency
from rireki.utils.time_helpers import now


class Driver(Configurable, HasFrequency):

    def __init__(self, name, traits=[]):
        Configurable.__init__(self, name, [HasFrequency] + traits)

    def has_pending_backups(self, last_backup_time):
        frequency_in_seconds = self.frequency * 60

        return last_backup_time < now() - frequency_in_seconds
