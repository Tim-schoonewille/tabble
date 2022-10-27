from flask import Blueprint

from app.constants import API_URL_PREFIX, HTTP_200_OK


auth = Blueprint('auth', __name__, url_prefix=API_URL_PREFIX + '/auth')

@auth.get('/test')
def test_route():
    return {"content":"Hello World"}, HTTP_200_OK
