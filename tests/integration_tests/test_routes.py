from unit_tests.setup import BaseTestCase


class TestRoutes(BaseTestCase):
    url_index = '/'
    url_show_summary = '/showSummary'
    url_purchase_places = '/purchasePlaces'
    url_logout = '/logout'

    def get_book_url(self, competition, club):
        return f"/book/{competition['name']}/{club['name']}"

    @classmethod
    def setUpClass(cls):
        super(TestRoutes, cls).setUpClass()
        cls.club = cls.clubs[0]
        cls.initial_club_points = int(cls.club['points'])
        cls.competition = cls.competitions[0]
        cls.initial_competition_places = int(cls.competition['numberOfPlaces'])

    @classmethod
    def tearDownClass(self):
        self.competition['numberOfPlaces'] = self.initial_competition_places
        self.competition['places_booked'][self.club['name']] = 0
        self.club['points'] = self.initial_club_points

    def test_login_purchase_logout(self):
        # Access index page
        response = self.client.get(
            self.url_index
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Welcome to the GUDLFT Registration Portal!',
            response.data
        )

        # Post email to log in
        data = {
            'email': self.club['email']
        }
        response = self.client.post(
            self.url_show_summary,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            f"Welcome, {self.club['email']}".encode('utf-8'),
            response.data
        )

        # Access booking page
        response = self.client.get(
            self.get_book_url(self.competition, self.club)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            (
                f"Booking for {self.competition['name']} || GUDLFT"
            ).encode('utf-8'),
            response.data
        )

        # Purchase 5 places
        places_to_book = 5
        data = {
            'club': self.club['name'],
            'competition': self.competition['name'],
            'places': places_to_book
        }
        response = self.client.post(
            self.url_purchase_places,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Great-booking complete!',
            response.data
        )
        self.assertIn(
            f"Welcome, {self.club['email']}".encode('utf-8'),
            response.data
        )

        # Logout
        response = self.client.get(
            self.url_logout,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Welcome to the GUDLFT Registration Portal!',
            response.data
        )

        # Points are updated
        self.assertEqual(
            self.club['points'],
            self.initial_club_points - places_to_book
        )
        self.assertEqual(
            self.competition['numberOfPlaces'],
            self.initial_competition_places - places_to_book
        )
        self.assertEqual(
            self.competition['places_booked'][self.club['name']],
            places_to_book
        )
