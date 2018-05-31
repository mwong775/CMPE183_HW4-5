# Here go your api methods.

import hashlib
from gluon.utils import web2py_uuid

SECRET_KEY = 'melanzana'

def check():
    response.headers['Access-Control-Allow-Origin'] = '*'
    youare = 'None' if logged_in_user is None else logged_in_user['username']
    return response.json(dict(result=youare))

def register():
    response.headers['Access-Control-Allow-Origin'] = '*'
    username = request.vars.username
    # Checks new.
    if not db(db.myuser.username == username).isempty():
        return response.json(dict(result='duplicate'))
    h = hashlib.sha256(SECRET_KEY)
    h.update(request.vars.password)
    token = web2py_uuid()
    # Inserts the user
    db.myuser.insert(
        username = username,
        password = h.hexdigest(),
        token = token,
    )
    # Creates the cookie.
    response.cookies['myapp'] = token
    response.cookies['myapp']['path'] = '/' # Valid in all the app
    response.cookies['myapp']['expires'] = 24 * 3600
    return response.json(dict(result='created'))

def login():
    response.headers['Access-Control-Allow-Origin'] = '*'
    username = request.vars.username
    h = hashlib.sha256(SECRET_KEY)
    h.update(request.vars.password)
    r = db((db.myuser.username == username) &
           (db.myuser.password == h.hexdigest())).select().first()
    if r is None:
        response.cookies['myapp'] = None
        return response.json(dict(result='fail'))
    # Creates a new token.
    token = web2py_uuid()
    r.update_record(token = token)
    # Puts it in the cookie.
    response.cookies['myapp'] = token
    response.cookies['myapp']['path'] = '/' # Valid in all the app
    response.cookies['myapp']['expires'] = 24 * 3600
    response.cookies['myapp']['secure'] = False # For testing only.
    return response.json(dict(result='logged in'))

def logout():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.cookies['myapp'] = None
    return response.json(dict(result='logged out'))



