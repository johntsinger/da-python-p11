from unittest import TestCase
import server


class TestLoadClubs(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestLoadClubs, cls).setUpClass()
        server.app.config['TESTING'] = True
        cls.expected_keys = ['name', 'email', 'points']

    def test_load_from_json(self):
        results = server.loadClubs()
        self.assertIsInstance(results, list)
        for elt in results:
            with self.subTest(elt=elt):
                self.assertIsInstance(elt, dict)
                self.assertEqual(
                    list(elt.keys()),
                    self.expected_keys
                )


class TestLoadCompetitions(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestLoadCompetitions, cls).setUpClass()
        server.app.config['TESTING'] = True
        cls.expected_keys = ['name', 'date', 'numberOfPlaces']

    def test_load_from_json(self):
        results = server.loadCompetitions()
        self.assertIsInstance(results, list)
        for elt in results:
            with self.subTest(elt=elt):
                self.assertIsInstance(elt, dict)
                self.assertEqual(
                    list(elt.keys()),
                    self.expected_keys
                )


class TestAddExtraFieldToCompetition(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestAddExtraFieldToCompetition, cls).setUpClass()
        server.app.config['TESTING'] = True
        cls.clubs = [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13"
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            },
        ]
        cls.competitions = [
            {
                "name": "Not out dated",
                "date": "2024-10-22 13:30:00",
                "numberOfPlaces": "13"
            },
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            }
        ]
        cls.expected_keys = [
            'name', 'date', 'numberOfPlaces', 'places_booked', 'is_active'
        ]

    def test_add_extra_fields(self):
        server.add_extra_fields_to_competition(
            self.competitions,
            self.clubs
        )
        for elt in self.competitions:
            with self.subTest(elt=elt):
                self.assertEqual(
                    list(elt.keys()),
                    self.expected_keys
                )
                self.assertIsInstance(elt['places_booked'], dict)
                self.assertIsInstance(elt['is_active'], bool)
                for club in self.clubs:
                    with self.subTest(club=club):
                        self.assertIn(
                            club['name'],
                            elt['places_booked'].keys()
                        )
                        self.assertEqual(
                            elt['places_booked'][club['name']],
                            0
                        )
