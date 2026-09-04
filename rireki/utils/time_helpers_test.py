from rireki.testing.test_case import TestCase
from rireki.utils.time_helpers import now, set_testing_now, DAY_SECONDS, YEAR_SECONDS


class TestTimeHelpers(TestCase):

    def tearDown(self):
        TestCase.tearDown(self)

        set_testing_now(None)

    def test_constants(self):
        assert DAY_SECONDS == 86400
        assert YEAR_SECONDS == 365 * DAY_SECONDS

    def test_now_and_testing_now(self):
        set_testing_now(1234567890)
        assert now() == 1234567890

        set_testing_now(None)
        assert now() != 1234567890
