from flask import Flask



from app.ext import db
from app.ext import jwt
from app.models import *


def create_app():

    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    jwt.init_app(app)
    
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.user_id
    
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(user_id=identity).one_or_none()

    
    from app.views.auth import auth
    
    app.register_blueprint(auth)

    return app
