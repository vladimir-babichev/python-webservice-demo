from datetime import date, datetime

from app.database import db
from app.models import User
from flask import request
from flask_restful import Resource
from sqlalchemy.sql import text


class UserAPI(Resource):
    def put(self, username):
        if not username.isalpha():
            return {"error": "Username must contain only letters."}, 400
        date_of_birth = request.json.get("dateOfBirth")

        if not date_of_birth:
            return {"error": "Date of birth is missing."}, 400
        try:
            date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format, should be YYYY-MM-DD."}, 400

        if date_of_birth >= date.today():
            return {"error": "Date of birth must be a date before today."}, 400

        user = User.query.filter_by(username=username).first()
        if user:
            user.date_of_birth = date_of_birth
        else:
            user = User(username=username, date_of_birth=date_of_birth)
            db.session.add(user)
        db.session.commit()
        return "", 204

    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"error": "User not found."}, 404

        today = date.today()
        birthday = user.date_of_birth.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)

        delta = birthday - today
        if delta.days == 0:
            message = f"Hello, {user.username}! Happy birthday!"
        else:
            message = (
                f"Hello, {user.username}! Your birthday is in {delta.days} day(s)."
            )
        return {"message": message}


class Status(Resource):
    def get(self):
        try:
            db.session.execute(text("SELECT 1"))
            # db.session.execute("SELECT 1")
            return {"status": "OK"}
        except Exception as e:
            return {"status": "DB connection error", "error": f"{str(e)}"}, 500
