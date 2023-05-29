"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from datetime import datetime
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

db.create_all()


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

    def test_message_model(self):
        """Does the basic message model work?"""

        # Create a user
        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(user)
        db.session.commit()

        # Create a message
        m = Message(
            text="text",
            timestamp=datetime.utcnow(),
            user_id=user.id
        )
        db.session.add(m)
        db.session.commit()

        self.assertEqual(m.text, "text")
        self.assertEqual(m.user_id, user.id)