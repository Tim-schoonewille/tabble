from flask import Flask
from flask import jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import verify_jwt_in_request


from datetime import timedelta
from functools import wraps
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
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2),
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


    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now()
            target_timestamp = datetime.timestamp(now + timedelta(minutes=1))
            
            if target_timestamp > exp_timestamp:
                
                # # add to database
                jti = get_jwt()["jti"]
                now = datetime.now()
                db.session.add(TokenBlocklist(jti=jti, created_at=now))
                db.session.commit()
                
                
                additional_claims = {
                    "is_admin": current_user.is_admin,
                    "is_mod": current_user.is_mod}
                
                access_token = create_access_token(identity=current_user, additional_claims=additional_claims, fresh=False)
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response  
    
    

    
    
    
    from app.views.auth import auth
    from app.views.tab import tab
    from app.views.favourites import favourites
    from app.views.artist import artist_bp
    from app.views.admin import admin_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(tab)
    app.register_blueprint(favourites)
    app.register_blueprint(artist_bp)  
    app.register_blueprint(admin_bp)  
    
    
    # with app.app_context():
    #     db.create_all()

    return app
