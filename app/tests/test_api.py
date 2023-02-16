import json
import unittest
from datetime import date, timedelta

from app.database import db
from app.models import User
from dateutil.relativedelta import relativedelta

from app.app import create_app


class UserAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_save_user_api(self):
        username = "testuser"
        User.query.filter_by(username=username).delete()
        response = self.client().put(
            f"/hello/{username}",
            data=json.dumps({"dateOfBirth": "2010-10-10"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

        user = User.query.filter_by(username=username).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, username)
        self.assertEqual(str(user.date_of_birth), "2010-10-10")

    def test_put_username_contains_only_letters(self):
        response = self.client().put(
            "/hello/test-user",
            data=json.dumps({"dateOfBirth": "2010-10-10"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = self.client().put(
            "/hello/test1",
            data=json.dumps({"dateOfBirth": "2010-10-10"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_put_username_date_is_before_today(self):
        response = self.client().put(
            "/hello/testuser",
            data=json.dumps({"dateOfBirth": f"{date.today()}"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = self.client().put(
            "/hello/testuser",
            data=json.dumps({"dateOfBirth": f"{date.today()+timedelta(1)}"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_get_user_api(self):
        username = "testuser"
        birthday = date.today() - relativedelta(days=2)
        User.query.filter_by(username=username).delete()
        db.session.commit()
        user = User(
            username=username,
            date_of_birth=birthday,
        )
        db.session.add(user)
        db.session.commit()

        response = self.client().get(f"/hello/{username}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("message", data)

        expected_delta = birthday.replace(year=date.today().year + 1) - date.today()
        self.assertEqual(
            data["message"],
            f"Hello, {username}! Your birthday is in {expected_delta.days} day(s).",
        )

    def test_get_user_happybirthday_greeting(self):
        username = "testuser"
        User.query.filter_by(username=username).delete()
        db.session.commit()
        user = User(
            username=username,
            date_of_birth=date.today() - relativedelta(years=1),
        )
        db.session.add(user)
        db.session.commit()

        response = self.client().get(f"/hello/{username}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("message", data)
        self.assertEqual(data["message"], f"Hello, {username}! Happy birthday!")


if __name__ == "__main__":
    unittest.main()
