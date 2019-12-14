class Project(object):

    def __init__(self, name, driver, storage):
        self.name = name
        self.driver = driver
        self.storage = storage

    def has_pending_backup(self):
        # Stub
        return True

    def backup(self):
        # Stub
        pass
