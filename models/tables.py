# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

# Product table.
db.define_table('product',
    Field('product_name'),
    Field('quantity', 'integer'),
    Field('price', 'double'),
    Field('image_url'),
    Field('description', 'text'),
)
db.product.id.readable = db.product.id.writable = False
db.product.image_url.requires = IS_URL()

import json

def nicefy(b):
    if b is None:
        return 'None'
    obj = json.loads(b)
    s = json.dumps(obj, indent=2)
    return s


def get_user_email():
    """Note that this function always returns a lowercase email address."""
    if request.env.web2py_runtime_gae:
        from google.appengine.api import users as googleusers
        u = googleusers.get_current_user()
        if u is None:
            return None
        else:
            return u.email().lower()
    else:
        if auth.user is None:
            return None
        else:
            return auth.user.email.lower()