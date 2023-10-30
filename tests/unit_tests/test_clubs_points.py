from unit_tests.setup import BaseTestCase


class TestClubsPoints(BaseTestCase):
    url = '/clubsPoints'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        for club in self.clubs:
            with self.subTest(club=club):
                self.assertIn(
                    f"{club['name']}".encode('utf-8'),
                    response.data
                )
                self.assertIn(
                    f"{club['points']}".encode('utf-8'),
                    response.data
                )
