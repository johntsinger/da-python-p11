from unit_tests.setup import BaseTestCase


class TestIndex(BaseTestCase):
    url = '/'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            200
        )
