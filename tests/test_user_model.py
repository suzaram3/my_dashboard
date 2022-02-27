import unittest
from app import create_app, db
from app.models import AnonymousUser, Role, Permission, User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)

    def test_password_setter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password="cat")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password="cat")
        self.assertTrue(u.verify_password("cat"))
        self.assertFalse(u.verify_password("dog"))

    def test_password_salts_are_random(self):
        u = User(password="cat")
        u2 = User(password="cat")
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_role(self):
        u = User(email='mitch@example.com', password='cat')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
        
    def test_anonymous_user(self):
        a = AnonymousUser()
        self.assertFalse(a.can(Permission.FOLLOW))
        self.assertFalse(a.can(Permission.COMMENT))
        self.assertFalse(a.can(Permission.WRITE))
        self.assertFalse(a.can(Permission.MODERATE))
        self.assertFalse(a.can(Permission.ADMIN))
