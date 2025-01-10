from rireki.core.configurable import Configurable
from rireki.utils.string_helpers import str_slug
from rireki.utils.time_helpers import YEAR_SECONDS
from rireki.core.retention_policy import RetentionPolicy


class Project(Configurable):

    def __init__(self, name, driver, store):
        Configurable.__init__(self, name)

        self.last_backups_retention = 7
        self.year_backups_retention = RetentionPolicy.MONTHLY
        self.ancient_backups_retention = RetentionPolicy.YEARLY
        self.driver = driver
        self.store = store

    @property
    def slug(self):
        return str_slug(self.name)

    def load_config(self, config):
        Configurable.load_config(self, config)

        year_retention = RetentionPolicy.from_string(config.get('year_backups_retention'))
        ancient_retention = RetentionPolicy.from_string(config.get('ancient_backups_retention'))

        self.last_backups_retention = config.get('last_backups_retention') or self.last_backups_retention
        self.year_backups_retention = year_retention or self.year_backups_retention
        self.ancient_backups_retention = ancient_retention or self.ancient_backups_retention

        self.driver.project = self
        self.store.project = self

        self.driver.load_config(config['driver'])
        self.store.load_config(config['store'])

    def get_config(self):
        config = Configurable.get_config(self)

        config['last_backups_retention'] = self.last_backups_retention
        config['year_backups_retention'] = self.year_backups_retention.value
        config['ancient_backups_retention'] = self.ancient_backups_retention.value
        config['driver'] = self.driver.get_config()
        config['store'] = self.store.get_config()

        return config

    def has_pending_backups(self):
        last_backup = self.get_last_backup()

        if not last_backup:
            return True

        return self.driver.has_pending_backups(last_backup.time)

    def get_backups(self):
        return self.store.get_backups()

    def get_last_backup(self):
        return self.store.get_last_backup()

    def get_stale_backups(self):
        backups = sorted(self.get_backups(), key=lambda x: x.time, reverse=True)
        year_retention = self.year_backups_retention
        ancient_retention = self.ancient_backups_retention
        retained_backups = []
        stale_backups = []

        for backup in backups:
            previous_backup = retained_backups[-1] if retained_backups else None
            retention_policy = year_retention if backup.get_age() < YEAR_SECONDS else ancient_retention

            if len(retained_backups) < self.last_backups_retention or backup.retain(previous_backup, retention_policy):
                retained_backups.append(backup)
                continue

            stale_backups.append(backup)

        return stale_backups

    def perform_backup(self):
        self.driver.perform_backup()

    def remove_backup(self, backup):
        self.store.remove_backup(backup)
