import unittest
from datetime import date, datetime, timedelta
from app import create_app, db
from app.models import Contact


class ContactModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_update_next_contact(self):
        """Testing update next contact date"""
        c = Contact(first="test", last="jones", frequency=4, last_contact="2022-01-01")
        db.session.add(c)
        c.update_next_contact()
        self.assertEqual(c.next_contact, ("2022-05-01"))
