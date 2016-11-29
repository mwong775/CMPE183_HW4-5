# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


db.define_table('rating',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('image_id', 'integer'),
                Field('num_stars', 'integer'),
                )


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
