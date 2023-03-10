from app.api import Status, UserAPI
from app.database import db
from flask import Flask
from flask_restful import Api


def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")
    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.add_resource(UserAPI, "/hello/<username>")
    api.add_resource(Status, "/status")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
