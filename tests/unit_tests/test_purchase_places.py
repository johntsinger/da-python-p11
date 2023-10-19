from unit_tests.setup import BaseTestCase


class TestPurchasePlaces(BaseTestCase):
    url = '/purchasePlaces'

    @classmethod
    def setUpClass(cls):
        super(TestPurchasePlaces, cls).setUpClass()
        cls.club = cls.clubs[0]
        cls.club_points = int(cls.club['points'])
        cls.competition = cls.competitions[0]

    def test_club_points_updated(self):
        places_booked = 5
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': places_booked
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.club['points'], self.club_points - places_booked)
