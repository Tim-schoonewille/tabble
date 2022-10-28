from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user

from app.constants import API_URL_PREFIX, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from app.ext import db
from app.models import Tab, Favourite


favourites = Blueprint('favourites', __name__, url_prefix=API_URL_PREFIX + '/favourites')


@favourites.get('/')
@jwt_required()
def get_favourites():
    if request.args:
        
        artist = request.args.get('artist')
        title = request.args.get('title')
        
        
        if artist:
            response = {"content": [favourite.serialize() for favourite in current_user.favourite_tabs if favourite.tab.artist.name==artist]}
            return response, HTTP_200_OK

        if title:
            response = {"content": [favourite.serialize() for favourite in current_user.favourite_tabs if favourite.tab.title==title]}
            return response, HTTP_200_OK          
    
    response = {"content": [favourite.serialize() for favourite in current_user.favourite_tabs]}
    return response, HTTP_200_OK