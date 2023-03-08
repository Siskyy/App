import unittest
from unittest import TestCase
from app import app

class TestApp(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_login_valid(self):
        response = self.app.post('/login', data={'username': 'marcbert', 'password': 'password'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')
        self.assertOnceCalledWith()

    def test_login_invalid_username(self):
        response = self.app.post('/login', data={'username': 'foo', 'password': 'password'})

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.location, '/')


    def test_login_invalid_password(self):
        response = self.app.post('/login', data={'username': 'marcbert', 'password': 'foo'})

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(response.location, '/')

    def test_search_no_input(self):
        response = self.app.post('/search', data={""})

        self.assertEqual()

unittest.main()