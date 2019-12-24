from rireki.testing.test_case import TestCase
from rireki.utils.string_helpers import str_slug


class TestStringHelpers(TestCase):

    def test_slug(self):
        assert str_slug('Miyamoto Musashi') == 'miyamoto-musashi'
        assert str_slug('Let\'s Go') == 'lets-go'
