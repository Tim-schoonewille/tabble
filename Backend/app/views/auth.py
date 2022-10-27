from flask import Blueprint
from flask import request
from werkzeug.security import generate_password_hash
from uuid import uuid4

from app.constants import API_URL_PREFIX, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from app.ext import db
from app.models import User


auth = Blueprint('auth', __name__, url_prefix=API_URL_PREFIX + '/auth')

@auth.get('/test')
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
