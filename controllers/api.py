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
    return response.json(dict(result='created', token=token))

def login():
    response.headers['Access-Control-Allow-Origin'] = '*'
    username = request.vars.username
    h = hashlib.sha256(SECRET_KEY)
    h.update(request.vars.password)
    r = db((db.myuser.username == username) &
           (db.myuser.password == h.hexdigest())).select().first()
    if r is None:
        return response.json(dict(result='fail'))
    # Creates a new token if needed.
    if r.token is None:
        token = web2py_uuid()
        r.update_record(token = token)
    else:
        token = r.token
    return response.json(dict(result='logged in', token=token))

def logout():
    response.headers['Access-Control-Allow-Origin'] = '*'
    logger.info("The user trying to logout is: %r" % logged_in_user)
    if logged_in_user is not None:
        r = db((db.myuser.username == logged_in_user['username'])).select().first()
        if r is None:
            r.update_record(token=None)
        return response.json(dict(result='logged out', token=None))
    return response.json(dict(result='who are you?', token=None))



