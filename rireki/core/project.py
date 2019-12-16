class Project(object):

    def __init__(self, name, driver, storage):
        self.name = name
        self.driver = driver
        self.storage = storage

    def has_pending_backups(self):
        last_backup = self.get_last_backup()

        if not last_backup:
            return True

        return self.driver.has_pending_backups(last_backup.time)

    def get_last_backup(self):
        return self.storage.get_last_backup()

    def backup(self):
        # Stub
        pass
