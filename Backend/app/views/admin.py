from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user

from app.constants import API_URL_PREFIX, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from app.ext import db
from app.models import User
from app.decorators import admin_required



admin_bp = Blueprint('admin', __name__, url_prefix=API_URL_PREFIX + '/admin')


@admin_bp.get('/user')
@admin_required()
def admin_get_users():
    
    all_users = User.query.all()
    
    response = {"content": [user.serialize() for user in all_users]}
    return response, HTTP_200_OK


@admin_bp.get('/user/<user_uuid>')
@admin_required()
def admin_get_user(user_uuid):
    
    user = User.query.filter_by(user_uuid=user_uuid).one_or_none()
    
    if not user:
        response = {"content":"No such user"}
        return response, HTTP_404_NOT_FOUND
    
    response = {"content": user.serialize()}
    return response, HTTP_200_OK


@admin_bp.put('/user/<user_uuid>/deactivate')
@admin_required()
def deactivate_user(user_uuid):
    user = User.query.filter_by(user_uuid=user_uuid).one_or_none()
    
    if not user:
        response = {"content":"No such user"}
        return response, HTTP_404_NOT_FOUND
    
    user.activated = False
    db.session.commit()
    
    response = {"content": f"User '{user.email}' deactivated"}    
    return response, HTTP_200_OK



    
    

