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
from app.models import Tab



tab = Blueprint('tab', __name__, url_prefix=API_URL_PREFIX + '/tab')


@tab.get('/')
def get_tabs():
    pass


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
    
    
    print(request.json)
    print(current_user)
    
    return {"content": "Hello world!"}