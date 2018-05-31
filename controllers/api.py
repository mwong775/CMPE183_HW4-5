# Here go your api methods.

def check_login():
    response.headers['Access-Control-Allow-Origin'] = '*'
    is_logged_in = logged_in_user is not None
    return response.json(dict(is_logged_in=is_logged_in))
