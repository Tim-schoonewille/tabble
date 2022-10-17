from flask import Flask
from app.ext import db



def create_app():

    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI = 'file:///db.sqlite3'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)

    return app
