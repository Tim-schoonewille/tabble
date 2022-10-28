from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user

from datetime import datetime
from uuid import uuid4

from app.constants import API_URL_PREFIX, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from app.ext import db
from app.models import Artist


artist_bp = Blueprint('artist', __name__, url_prefix=API_URL_PREFIX + '/artist')


@artist_bp.get('/')
def get_all_artists():
    
    all_artists = Artist.query.all()

    response = {"content": [artist.serialize() for artist in all_artists]}
    return response, HTTP_200_OK


@artist_bp.get('/<name>')
def get_artist_by_name(name):
    
    artist = Artist.query.filter_by(name=name.lower()).one_or_none()
    
    if not artist:
        response = {"content": "Artist does not exist"}
        return response, HTTP_404_NOT_FOUND
    
    
    response = {"content": artist.serialize()}
    return response, HTTP_200_OK







