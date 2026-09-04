import os
import tempfile

from rireki.core.driver import Driver
from rireki.core.project import Project
from rireki.stores.local import Local
from rireki.testing.test_case import TestCase
from rireki.utils.time_helpers import set_testing_now


class DummyDriver(Driver):
    NAME = 'dummy'

    def _prepare_backup_files(self, path):
        return path


class TestDriver(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self.driver = DummyDriver()
        self.store = Local()
        self.project = Project('test-project', self.driver, self.store)
        self.driver.project = self.project

    def test_create_and_clean_temporary_folder(self):
        tmp_folder = self.driver._create_temporary_folder()

        assert os.path.exists(tmp_folder)
        assert os.path.isdir(tmp_folder)
        assert os.path.commonpath([tmp_folder, tempfile.gettempdir()]) == tempfile.gettempdir()
        assert os.path.basename(tmp_folder).startswith('rireki-dummy-test-project-')

        self.driver._clean_backup_files(tmp_folder)

        assert not os.path.exists(tmp_folder)

    def test_has_pending_backups(self):
        self.driver.frequency = 60  # 60 minutes = 3600 seconds
        current_time = 1000000
        set_testing_now(current_time)

        try:
            # 3601 seconds ago -> pending
            assert self.driver.has_pending_backups(current_time - 3601) is True
            # 3599 seconds ago -> not pending
            assert self.driver.has_pending_backups(current_time - 3599) is False
        finally:
            set_testing_now(None)
