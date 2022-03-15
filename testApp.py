from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True


    def tearDown(self):
      """Stuff to do after each test."""

    def test_session_info(self):
        with app.test_client() as client:
            resp = client.get("/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(session['count'], 1)
        
    def test_homepage(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertIn(b'<title>Alcohol</title>', resp.data)


