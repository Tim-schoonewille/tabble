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
import string
import random

from app.constants import API_URL_PREFIX, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from app.ext import db
from app.models import TokenBlocklist, User, Registration


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
                    is_admin=False,
                    is_mod=True,
                    )
    

    
    db.session.add(new_user)
    db.session.commit()
    
    reg_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    print(reg_string)
    print(new_user.user_uuid)
    
    new_registration_confirm = Registration(user_id=new_user.user_id,
                                            registration_string=reg_string)
    
    db.session.add(new_registration_confirm)
    db.session.commit()
                                               

    response = {"content":"Registration success"}
    return response, HTTP_201_CREATED



@auth.post('/login')
def login_user():
    
    user = User.query.filter_by(email=request.json.get('email').lower()).one_or_none()
    
    if not user or not check_password_hash(user.password, request.json.get('password')):
        response = {"content":"Invalid email/password!"}
        return response, HTTP_401_UNAUTHORIZED
    
    if not user.activated:
        response = {"content":"Account not activated."}
        return response, HTTP_400_BAD_REQUEST
    
    response = jsonify(content="Login success.")
    
    additional_claims = {
        "is_admin": user.is_admin,
        "is_mod": user.is_mod
    }
    
    access_token = create_access_token(identity=user, 
                                       additional_claims=additional_claims,
                                       fresh=True)
    
    set_access_cookies(response, access_token)
    
    user.last_login = datetime.utcnow()
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


@auth.post('/<user_uuid>/confirm/<registration_string>')
def confirm_registration(user_uuid, registration_string):
    
    user = User.query.filter_by(user_uuid=user_uuid).one_or_none()
    registration = Registration.query.filter_by(user_id=user.user_id).one_or_none()
    
    if not user or not registration:
        return {"content": "Invalid user"}, HTTP_404_NOT_FOUND
    
    if user.activated:
        return {"content": "Already activated"}, HTTP_400_BAD_REQUEST
    
    if registration.registration_string != registration_string:
        return {"content": "Invalid string"}, HTTP_400_BAD_REQUEST
    
    user.activated = True
    registration.date_confirmed = datetime.utcnow()
    registration.completed = True
    
    db.session.commit()
    
    return {"message": "Account confirmed!"}


@auth.post('/<user_uuid>/confirm/new')
def request_new_confirm(user_uuid):
    
    user = User.query.filter_by(user_uuid=user_uuid).one_or_none()
    
    if user.activated:
        return {"content": "Already activated."}, HTTP_400_BAD_REQUEST
    
    registration = Registration.query.filter_by(user_id=user.user_id).one_or_none()
    
    if not registration:
        return {"content": "No initial registration"}, HTTP_400_BAD_REQUEST
    
    db.session.delete(registration)
    db.session.commit()
    
    reg_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    print(reg_string)
    print(user.user_uuid)
    
    new_registration_confirm = Registration(user_id=user.user_id,
                                            registration_string=reg_string)
    
    db.session.add(new_registration_confirm)
    db.session.commit()
    
    response = {"content": "New confirmation send!"}
    return response, HTTP_200_OK