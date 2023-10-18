from unittest import TestCase
from server import app, clubs, competitions


class ClientMixin:
    @classmethod
    def setUpClass(cls):
        super(ClientMixin, cls).setUpClass()
        cls.client = app.test_client()


class BaseTestCase(ClientMixin, TestCase):
    clubs = clubs
    competitions = competitions
