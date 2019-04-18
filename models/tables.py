# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

# logger.info("The user record is: %r" % auth.user)

import datetime

def get_user_email():
    return None if auth.user is None else auth.user.email

def get_current_time():
    return datetime.datetime.utcnow()

db.define_table('post',
                Field('post_author', default=get_user_email()),
                Field('post_title'), # At most 512 characters
                Field('post_content', 'text'), # "unlimited"
                Field('post_time', 'datetime', update=get_current_time()),
                )

db.post.post_time.readable = True
db.post.post_time.writable = False
db.post.post_author.writable = False
db.post.id.readable = False
db.post.post_title.label = T('Title')
db.post.post_author.label = T('Author email')
# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# Stars

db.define_table('star',
                Field('user_id', 'reference auth_user'), # The user who starred
                Field('post_id', 'reference post'), # The starred post
                )