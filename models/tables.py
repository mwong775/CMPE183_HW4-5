# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


# Super minimal authentication.
db.define_table('myusers',
                Field('username'),
                Field('password'),
                Field('token'),
                )

# Gets the identity of the logged in user.
logged_in_user = None
cookie = request.cookies.get('myapp')
if cookie is not None:
    r = db(db.myuser.token == cookie).first()
    if r is not None:
        logged_in_user = dict(
            id = r.id,
            name = r.username
        )

