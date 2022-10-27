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
from app.models import Tab, Favourite



tab = Blueprint('tab', __name__, url_prefix=API_URL_PREFIX + '/tab')


@tab.get('/')
def get_tabs():
    
    all_tabs = Tab.query.all()
    print(all_tabs)
    
    response = {"content": [tab.serialize() for tab in all_tabs]}
    return response, HTTP_200_OK
    


@tab.post('/')
@jwt_required()
def add_tab():
    link_to_tab = request.json.get('link_to_tab')
    
    if not link_to_tab:
        response = {"content": "Provide a valid link"}
        return response, HTTP_400_BAD_REQUEST
    
    if Tab.query.filter_by(link_to_tab=link_to_tab).one_or_none():
        response = {"content": "Tab already in app"}
        return response, HTTP_409_CONFLICT
    
    
    new_tab = Tab(tab_uuid=str(uuid4()),
                  user=current_user,
                  artist=request.json.get('artist'),
                  title=request.json.get('title'),
                  tab=request.json.get('tab'),
                  link_to_tab=link_to_tab)
    
    db.session.add(new_tab)
    db.session.commit()
    new_tab.favourite(current_user)

    
    return {"content": "Tab added and favorited."}, HTTP_200_OK


@tab.get('/<tab_uuid>')
def get_specific_tab(tab_uuid):
    
    specific_tab = Tab.query.filter_by(tab_uuid=tab_uuid).one_or_none()
    
    if not specific_tab:
        response = {"content":"Invalid tab ID"}
        return response, HTTP_404_NOT_FOUND

    response = {"content":specific_tab.serialize()}

    return response, HTTP_200_OK


@tab.put('/<tab_uuid>')
@jwt_required()
def edit_specific_tab(tab_uuid):

    specific_tab = Tab.query.filter_by(tab_uuid=tab_uuid).one_or_none()
    
    
    if not specific_tab:
        response = {"content":"Invalid tab ID"}
        return response, HTTP_404_NOT_FOUND
    
    
    if specific_tab.user != current_user:
        response = {"content":"You can't edit this tab."}
        return response, HTTP_401_UNAUTHORIZED
    
    
    specific_tab.artist = request.json.get('artist') or specific_tab.artist
    specific_tab.title = request.json.get('title') or specific_tab.title
    specific_tab.link_to_tab = request.json.get('link_to_tab') or specific_tab.link_to_tab
    specific_tab.tab = request.json.get('tab') or specific_tab.tab
    
    
    db.session.commit()
    
    
    response = {"content": "Tab updated!"}
    return response, HTTP_200_OK



@tab.delete('/<tab_uuid>')
@jwt_required()
def delete_tab(tab_uuid):

    specific_tab = Tab.query.filter_by(tab_uuid=tab_uuid).one_or_none()
    
    
    if not specific_tab:
        response = {"content":"Invalid tab ID"}
        return response, HTTP_404_NOT_FOUND
    
    
    if specific_tab.user != current_user:
        response = {"content":"You can't edit this tab."}
        return response, HTTP_401_UNAUTHORIZED
    
    
    db.session.delete(specific_tab)
    db.session.commit()
    
    response = {"content":"Tab deleted"}
    return response, HTTP_200_OK


@tab.post('/<tab_uuid>/favourite')
@jwt_required()
def add_tab_to_favourite(tab_uuid):

    specific_tab = Tab.query.filter_by(tab_uuid=tab_uuid).one_or_none()
    
    
    if not specific_tab:
        response = {"content":"Invalid tab ID"}
        return response, HTTP_404_NOT_FOUND
    
    
    if Favourite.query.filter_by(tab_uuid=tab_uuid,
                                 user_id=current_user.user_id).one_or_none():
        response = {"content": "already in favourite"}
        return response, HTTP_400_BAD_REQUEST
    
    specific_tab.favourite(current_user)
    response = {"content": "Tab added to favourites."}
    return response, HTTP_200_OK


@tab.delete('/<tab_uuid>/favourite')
@jwt_required()
def delete_tab_from_favourites(tab_uuid):

    specific_tab = Tab.query.filter_by(tab_uuid=tab_uuid).one_or_none()
    
    
    if not specific_tab:
        response = {"content":"Invalid tab ID"}
        return response, HTTP_404_NOT_FOUND
    
    favourite_tab = Favourite.query.filter_by(tab_uuid=tab_uuid,
                                 user_id=current_user.user_id).one_or_none()
    
    if not favourite_tab:
        response = {"content": "Not in list of favourites"}
        return response, HTTP_400_BAD_REQUEST
    
    db.session.delete(favourite_tab)
    db.session.commit()
    
    response = {"content": "Removed from favourites."}
    return response, HTTP_200_OK


@tab.post('/<tab_uuid>/complete')
@jwt_required()
def complete_tab(tab_uuid):
    
    favourite = Favourite.query.filter_by(tab_uuid=tab_uuid,
                                          user=current_user).one_or_none()
    
    if not favourite:
        response = {"content": "Can't complete because it is not favourited."}
        return response, HTTP_400_BAD_REQUEST
    
    favourite.completed = True
    
    db.session.commit()
    
    response = {"content": "Tab completed!"}
    return response, HTTP_200_OK


@tab.delete('/<tab_uuid>/complete')
@jwt_required()
def uncomplete_tab(tab_uuid):
    
    favourite = Favourite.query.filter_by(tab_uuid=tab_uuid,
                                          user=current_user).one_or_none()
    
    if not favourite:
        response = {"content": "Can't uncomplete because it is not favourited."}
        return response, HTTP_400_BAD_REQUEST

    favourite.completed = False
    
    db.session.commit()
    
    response = {"content": "Tab uncompleted!"}
    return response, HTTP_200_OK