"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()


        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_method(self):
        """Does __repr__ work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit

        expected_repr = f"<User #{u.id}: {u.username}, {u.email}>"
        actual_repr = u.__repr__()

        self.assertEqual(actual_repr, expected_repr)

    def test_is_following(self):
        """Test is_following method"""

        # Create two users
        user1 = User(username="user1", email="user1@example.com", password="password1")
        user2 = User(username="user2", email="user2@example.com", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Check if user1 is following user2 (should be False)
        is_following = user1.is_following(user2)
        self.assertFalse(is_following)

        # Set up the relationship where user1 follows user2
        user1.following.append(user2)
        db.session.commit()

        # Check if user1 is following user2 (should be True)
        is_following = user1.is_following(user2)
        self.assertTrue(is_following)

    def test_is_followed_by(self):
        """Test is_followed_by method"""

        # Create two users
        user1 = User(username="user1", email="user1@example.com", password="password1")
        user2 = User(username="user2", email="user2@example.com", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Check if user1 is followed by user2 (should be False)
        is_followed_by = user1.is_followed_by(user2)
        self.assertFalse(is_followed_by)

        # Set up the relationship where user2 follows user1
        user2.following.append(user1)
        db.session.commit()

        # Check if user1 is followed by user2 (should be True)
        is_followed_by = user1.is_followed_by(user2)
        self.assertTrue(is_followed_by)

    def test_create_new_user(self):
        """Test if User.signup successfully creates a new user with valid credentials."""
        # Create a new user
        user = User.signup(username="testuser", email="test@test.com", password="password", image_url=None)

        # Check if the user is successfully created
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")

    def test_create_new_user_with_invalid_credentials(self):
        """Test if User.signup fails to create a new user if validations fail."""
        # Create a user
        user = User.signup(username="testuser1", email="test@test.com", password="password1", image_url=None)
        db.session.add(user)
        db.session.commit()

        # Attempt to create another user with the same email
        with self.assertRaises(Exception):
            user = User.signup(username="testuser2", email="test@test.com", password="password2", image_url=None)
            db.session.add(user)
            db.session.commit()

        # Create a user with missing username
        with self.assertRaises(Exception):
            user = User.signup(username=None, email="test2@test.com", password="password", image_url=None)
            db.session.add(user)
            db.session.commit()

        # Create a user with missing email
        with self.assertRaises(Exception):
            user = User.signup(username="testuser3", email=None, password="password", image_url=None)
            db.session.add(user)
            db.session.commit()

        # Create a user with missing password
        with self.assertRaises(Exception):
            user = User.signup(username="testuser4", email="test4@test.com", password=None, image_url=None)
            db.session.add(user)
            db.session.commit()

    def test_authenticate(self):
        # Create a user with valid credentials
        user = User.signup(username="testuser", email="test@test.com", password="password", image_url=None)
        db.session.commit()

        # Attempt to authenticate with valid credentials
        authenticated_user = User.authenticate(username="testuser", password="password")

        # Assert that the authenticated user is the same as the original user
        self.assertEqual(authenticated_user, user)

        # Attempt to authenticate with an invalid username
        authenticated_user = User.authenticate(username="invalidusername", password="password")

        # Assert that the authenticated user is None
        self.assertFalse(authenticated_user)

        # Attempt to authenticate with an invalid password
        authenticated_user = User.authenticate(username="testuser", password="invalidpassword")

        # Assert that the authenticated user is None
        self.assertFalse(authenticated_user)