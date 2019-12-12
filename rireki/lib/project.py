class Project(object):

    def __init__(self, name, driver):
        self.name = name
        self.driver = driver

    def has_pending_backup(self):
        # Stub
        return True

    def backup(self):
        # Stub
        pass
