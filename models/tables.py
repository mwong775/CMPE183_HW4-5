# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

db.create_table('priviledge',
                Field('user_email'),
                Field('city'),
                Field('permission'),
                )

db.priviledge.permission.requires = IS_IN_SET(['admin', 'edit', 'view', 'none'])

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
