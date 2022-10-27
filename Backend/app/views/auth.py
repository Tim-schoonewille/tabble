from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from flask_jwt_extended import unset_access_cookies
from uuid import uuid4
from datetime import datetime

from app.constants import API_URL_PREFIX, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from app.ext import db
from app.models import TokenBlocklist, User


auth = Blueprint('auth', __name__, url_prefix=API_URL_PREFIX + '/auth')

@auth.get('/test')
@jwt_required()
def test_route():
    return {"content":"Hello World"}, HTTP_200_OK


@auth.post('/register')
def register_account():
    
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')
    
    if not email or not password or password != confirm_password:
        response = {"content":"Invalid input"}
        return response, HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).one_or_none():
        response = {"content":"Email already in DB"}
        return response, HTTP_409_CONFLICT
    
    new_user = User(user_uuid=str(uuid4()),
                    email=email.lower(),
                    password=generate_password_hash(password),
                    is_admin=True,
                    is_mod=True,
                    )
    
    db.session.add(new_user)
    db.session.commit()
    
    response = {"conent":"Registration success"}
    return response, HTTP_201_CREATED



@auth.post('/login')
def login_user():
    
    user = User.query.filter_by(email=request.json.get('email').lower()).one_or_none()
    
    if not user or not check_password_hash(user.password, request.json.get('password')):
        response = {"content":"Invalid email/password!"}
        return response, HTTP_401_UNAUTHORIZED
    
    response = jsonify(content="Login success.")
    
    additional_claims = {
        "is_admin": user.is_admin,
        "is_mod": user.is_mod
    }
    
    access_token = create_access_token(identity=user, 
                                       additional_claims=additional_claims,
                                       fresh=True)
    
    set_access_cookies(response, access_token)
    
    user.last_login = datetime.now()
    db.session.commit()
    
    return response, HTTP_200_OK


@auth.post('/logout')
@jwt_required()
def auth_logout():
    
    jti = get_jwt()["jti"]
    now = datetime.now()
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    
    response = jsonify(content="Logout successfull")
    unset_access_cookies(response)
    
    return response, HTTP_200_OK

    
