from unit_tests.setup import BaseTestCase


class TestLogout(BaseTestCase):
    url = '/logout'

    def test_get(self):
        response = self.client.get(
            self.url,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Welcome to the GUDLFT Registration Portal!',
            response.data
        )
