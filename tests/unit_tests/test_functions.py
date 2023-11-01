from unittest import TestCase
import server


class TestLoadClubs(TestCase):
    @classmethod
    def setUpClass(cls):
        server.app.config['TESTING'] = True

    def test_load_from_json(self):
        expected_keys = ['name', 'email', 'points']
        results = server.loadClubs()
        self.assertIsInstance(results, list)
        self.assertTrue(results)
        for elt in results:
            with self.subTest(elt=elt):
                self.assertIsInstance(elt, dict)
                self.assertEqual(
                    list(elt.keys()),
                    expected_keys
                )


class TestLoadCompetitions(TestCase):
    @classmethod
    def setUpClass(cls):
        server.app.config['TESTING'] = True

    def test_load_from_json(self):
        expected_keys = ['name', 'date', 'numberOfPlaces']
        results = server.loadCompetitions()
        self.assertIsInstance(results, list)
        self.assertTrue(results)
        for elt in results:
            with self.subTest(elt=elt):
                self.assertIsInstance(elt, dict)
                self.assertEqual(
                    list(elt.keys()),
                    expected_keys
                )


class TestAddExtraFieldsToCompetition(TestCase):
    @classmethod
    def setUpClass(cls):
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
        for competition in self.competitions:
            with self.subTest(competition=competition):
                self.assertEqual(
                    list(competition.keys()),
                    self.expected_keys
                )
                self.assertIsInstance(competition['places_booked'], dict)
                self.assertIsInstance(competition['is_active'], bool)
                for i, (key, value) in enumerate(
                    competition['places_booked'].items()
                ):
                    with self.subTest(club=self.clubs[i]):
                        self.assertEqual(
                            (key, value),
                            (self.clubs[i]['name'], 0)
                        )
