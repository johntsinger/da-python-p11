from unit_tests.setup import BaseTestCase


class TestBook(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestBook, cls).setUpClass()
        cls.club = cls.clubs[0]
        cls.competition = cls.competitions[0]
        cls.past_competition = cls.competitions[2]

    def get_url(self, competition, club):
        return f"/book/{competition['name']}/{club['name']}"

    def test_get(self):
        response = self.client.get(
            self.get_url(self.competition, self.club)
        )
        self.assertEqual(response.status_code, 200)

    def test_wrong_competitons(self):
        competition = {'name': 'Wrong name'}
        response = self.client.get(
            self.get_url(competition, self.club),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Something went wrong-please try again",
            response.data
        )
        self.assertIn(
            b"Welcome to the GUDLFT Registration Portal!",
            response.data
        )

    def test_wrong_club(self):
        club = {'name': 'Wrong name'}
        response = self.client.get(
            self.get_url(self.competition, club),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Something went wrong-please try again",
            response.data
        )

    def test_access_past_competition(self):
        response = self.client.get(
            self.get_url(self.past_competition, self.club),
        )
        self.assertIn(
            (
                "You can not book places in a "
                "competition that has already taken place"
            ).encode('utf-8'),
            response.data
        )
        self.assertIn(
            f"Welcome, {self.club['email']}".encode('utf-8'),
            response.data
        )
