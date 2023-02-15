from flask import Flask
from flask_restful import Api

from app.api import UserAPI
from app.database import db


def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")
    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.add_resource(UserAPI, "/hello/<username>")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
