import os
from unittest import TestCase
from models import db, connect_db, User


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app, CURR_USER_KEY


db.create_all()


app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users."""

    
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_signup(self):
        """Can a user sign up?"""

        resp = self.client.post("/signup",
                                data={"username": "newuser",
                                      "email": "newuser@test.com",
                                      "password": "password"},
                                follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"@newuser", resp.data)

    def test_login(self):
        """Can a user log in?"""

        resp = self.client.post("/login",
                                data={"username": "testuser",
                                      "password": "testuser"},
                                follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Hello, testuser!", resp.data)

    def test_logout(self):
        """Can a user log out?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/logout", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(CURR_USER_KEY, self.client.session)

