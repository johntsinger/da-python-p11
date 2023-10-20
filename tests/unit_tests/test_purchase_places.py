from unit_tests.setup import BaseTestCase


class TestPurchasePlaces(BaseTestCase):
    url = '/purchasePlaces'

    @classmethod
    def setUpClass(cls):
        super(TestPurchasePlaces, cls).setUpClass()
        cls.club = cls.clubs[0]
        cls.initial_club_points = int(cls.club['points'])
        cls.competition = cls.competitions[0]
        cls.initial_competition_places = int(cls.competition['numberOfPlaces'])

    def tearDown(self):
        self.competition['numberOfPlaces'] = self.initial_competition_places
        self.club['points'] = self.initial_club_points

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
        self.assertEqual(
            self.club['points'],
            self.initial_club_points - places_booked
        )

    def test_purchase_less_places_than_club_has_points(self):
        places_booked = self.initial_club_points - 5
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
        self.assertEqual(
            self.club['points'],
            self.initial_club_points - places_booked
        )
        self.assertIn(
            b'Great-booking complete!',
            response.data
        )
        self.assertTrue(
            int(self.club['points']) >= 0
        )

    def test_purchase_more_places_than_club_has_points(self):
        places_booked = self.initial_club_points + 5
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': places_booked
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            int(self.club['points']) >= 0
        )
        self.assertEqual(
            self.club['points'],
            self.initial_club_points
        )
        self.assertIn(
            b'You do not have enough points.',
            response.data
        )
