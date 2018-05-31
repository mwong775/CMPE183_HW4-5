# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


# Super minimal authentication.
db.define_table('myuser',
                Field('username'),
                Field('password'),
                Field('token'),
                )

# For testing ONLY, so we can use insecure tokens.
session._secure = False

# Gets the identity of the logged in user.
logged_in_user = None
if request.cookies.has_key('myapp'):
    cookie = request.cookies['myapp'].value
    logger.info("Cookie: %r" % cookie)
    if cookie is not None:
        r = db(db.myuser.token == cookie).first()
        if r is not None:
            logged_in_user = dict(
                id = r.id,
                name = r.username
            )

