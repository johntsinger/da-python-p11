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
        self.competition['places_booked'][self.club['name']] = 0
        self.club['points'] = self.initial_club_points

    def test_club_points_updated(self):
        places_to_book = 5
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': places_to_book
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.club['points'],
            self.initial_club_points - places_to_book
        )

    def test_purchase_less_places_than_club_has_points(self):
        places_to_book = self.club['points'] - 5
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': places_to_book
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.club['points'],
            self.initial_club_points - places_to_book
        )
        self.assertIn(
            b'Great-booking complete!',
            response.data
        )
        self.assertTrue(
            int(self.club['points']) >= 0
        )

    def test_purchase_more_places_than_club_has_points(self):
        places_to_book = self.club['points'] + 5
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': places_to_book
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

    def test_post_without_data(self):
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': ''
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'You must enter a positive number of places to book them.',
            response.data
        )

    def test_purchase_negative_amount_of_places(self):
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': '-5'
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'You must enter a positive number of places to book them.',
            response.data
        )
        self.assertEqual(
            self.club['points'],
            self.initial_club_points
        )
        self.assertEqual(
            self.competition['numberOfPlaces'],
            self.initial_competition_places
        )

    def test_purchase_null_amount_of_places(self):
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': '0'
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'You must enter a positive number of places to book them.',
            response.data
        )
        self.assertEqual(
            self.club['points'],
            self.initial_club_points
        )
        self.assertEqual(
            self.competition['numberOfPlaces'],
            self.initial_competition_places
        )

    def test_purchase_more_than_max_per_competition_at_once(self):
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': self.club['points']
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            (
                f'You can not book more than {self.MAXIMUM_BOOKING_PER_CLUB}'
                ' places per competition.'
            ).encode('utf-8'),
            response.data
        )
        self.assertEqual(
            self.club['points'],
            self.initial_club_points
        )
        self.assertEqual(
            self.competition['numberOfPlaces'],
            self.initial_competition_places
        )

    def test_purchase_more_than_max_per_competition_several_steps(self):
        places_booked = 10
        self.competition['places_booked'][self.club['name']] = (
            places_booked
        )
        self.competition['numberOfPlaces'] -= places_booked
        self.club['points'] -= places_booked
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': self.club['points']
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            (
                'You can purchases no more than '
                f'{self.MAXIMUM_BOOKING_PER_CLUB - places_booked}'
                ' places as your club has already purchased'
                f' {places_booked} of them'
            ).encode('utf-8'),
            response.data
        )
        self.assertEqual(
            self.club['points'],
            self.initial_club_points - places_booked
        )
        self.assertEqual(
            self.competition['numberOfPlaces'],
            self.initial_competition_places - places_booked
        )

    def test_purchase_when_max_per_competition_has_been_reached(self):
        self.competition['places_booked'][self.club['name']] = (
            self.MAXIMUM_BOOKING_PER_CLUB
        )
        self.competition['numberOfPlaces'] -= self.MAXIMUM_BOOKING_PER_CLUB
        self.club['points'] -= self.MAXIMUM_BOOKING_PER_CLUB
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': self.club['points']
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            (
                'You have already reached the maximum'
                ' number of places for this competition'
            ).encode('utf-8'),
            response.data
        )
        self.assertEqual(
            self.club['points'],
            self.initial_club_points - self.MAXIMUM_BOOKING_PER_CLUB
        )
        self.assertEqual(
            self.competition['numberOfPlaces'],
            self.initial_competition_places - self.MAXIMUM_BOOKING_PER_CLUB
        )
