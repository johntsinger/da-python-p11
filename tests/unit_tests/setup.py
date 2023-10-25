from unittest import TestCase
import server


class ClientMixin:
    @classmethod
    def setUpClass(cls):
        super(ClientMixin, cls).setUpClass()
        server.app.config['TESTING'] = True
        cls.client = server.app.test_client()
        server.clubs = cls.clubs
        server.competitions = cls.competitions


class BaseTestCase(ClientMixin, TestCase):
    MAXIMUM_BOOKING_PER_CLUB = server.MAXIMUM_BOOKING_PER_CLUB
    clubs = [
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
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2024-10-22 13:30:00",
            "numberOfPlaces": "5"
        },
        {
            "name": "Past Comp",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "7"
        }

    ]
    server.add_extra_fields_to_competition(competitions, clubs)
