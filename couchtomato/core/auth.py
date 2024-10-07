from couchtomato.environment import Env
from flask import request, Response
from functools import wraps

def check_auth(username, password):
    return username == Env.setting('username') and password == Env.setting('password')

def authenticate():
    return Response(
        'This is not the page you are looking for. *waves hand*', 401,
        {'WWW-Authenticate': 'Basic realm="CouchTomato Login"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if Env.setting('username') and (not auth or not check_auth(auth.username, auth.password)):
            return authenticate()
        return f(*args, **kwargs)
    return decorated