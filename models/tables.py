# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

# Host we use for attacks.
ATTACK_HOST = "http://127.0.0.1:8000"

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('stolen_emails',
                Field('stolen_email'),
                )
