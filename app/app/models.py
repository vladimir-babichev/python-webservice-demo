from app.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username

    def __str__(self):
        return f"Username: {self.username}, Date of Birth: {self.date_of_birth}"
