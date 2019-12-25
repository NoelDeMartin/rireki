from rireki.utils.string_helpers import str_slug


class Project(object):

    def __init__(self, name, driver, store):
        self.name = name
        self.driver = driver
        self.store = store

    @property
    def slug(self):
        return str_slug(self.name)

    def has_pending_backups(self):
        last_backup = self.get_last_backup()

        if not last_backup:
            return True

        return self.driver.has_pending_backups(last_backup.time)

    def get_backups(self):
        return self.store.get_backups()

    def get_last_backup(self):
        return self.store.get_last_backup()

    def perform_backup(self):
        self.driver.perform_backup()
