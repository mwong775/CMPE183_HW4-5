# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

def get_user_email():
    return None if auth.user is None else auth.user.email

db.define_table('my_table',
    Field('the_title'),
    Field('the_text'),
    Field('the_user', default=get_user_email())
    )


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
