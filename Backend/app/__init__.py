from flask import Flask


from datetime import timedelta
from app.ext import db
from app.ext import jwt
from app.models import *


def create_app():

    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        JWT_SECRET_KEY = 'dev',
        JWT_COOKIE_CSRF_PROTECT = False,
        JWT_COOKIE_DOMAIN = 'dev.tabble',
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15),
        JWT_COOKIE_SECURE = False,
        JWT_TOKEN_LOCATION = ['cookies', 'headers']
        
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


    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None
    
    
    from app.views.auth import auth
    from app.views.tab import tab
    from app.views.favourites import favourites
    from app.views.artist import artist_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(tab)
    app.register_blueprint(favourites)
    app.register_blueprint(artist_bp)  
    
    # with app.app_context():
    #     db.create_all()

    return app
