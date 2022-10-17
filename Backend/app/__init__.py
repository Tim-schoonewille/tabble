from flask import Flask
from app.ext import db
from app.models import *


def create_app():

    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
