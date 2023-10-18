from unit_tests.setup import BaseTestCase


class TestShowSummary(BaseTestCase):
    url = '/showSummary'

    def test_post_valid_email(self):
        email = self.clubs[0]['email']
        response = self.client.post(
            self.url,
            data={
                'email': email
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes(email, 'utf-8'), response.data)

    def test_post_without_email(self):
        response = self.client.post(
            self.url,
            data={
                'email': ""
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Please, enter an email adress to continue",
            response.data
        )

    def test_post_not_available_email(self):
        response = self.client.post(
            self.url,
            data={
                'email': "test@test.com"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Sorry, that email was not found.",
            response.data
        )
