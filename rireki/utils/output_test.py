from rireki.testing.test_case import TestCase
from rireki.utils.output import format_time


class TestOutput(TestCase):

    def test_format_time_interval(self):
        assert format_time(1, 'interval') == '1 second'
        assert format_time(42, 'interval') == '42 seconds'
        assert format_time(61, 'interval') == '1 minute'
        assert format_time(150, 'interval') == '2 minutes'
        assert format_time(3601, 'interval') == '1 hour'
        assert format_time(14423, 'interval') == '4 hours'
        assert format_time(86412, 'interval') == '1 day'
        assert format_time(259211, 'interval') == '3 days'
        assert format_time(3628811, 'interval') == '42 days'
