# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
import datetime

def get_user_email():
	return None if auth.user is None else auth.user.email

def get_current_time():
    return datetime.datetime.utcnow()

def get_user_name():
	return None if auth.user is None else auth.user.first_name + " " + auth.user.last_name


db.define_table('product',
				Field('product_name'),
				Field('product_description', 'text'),
				Field('product_price', 'float'),
				Field('avg_rating', 'integer', default=0),
				)

db.product.avg_rating.readable= False;
db.product.avg_rating.writable= False;
db.product.product_name.label = T('Name')
db.product.product_price.label = T('Price')

db.define_table('reviews',
				Field('review_author', default=get_user_name()),
				Field('review_content', 'text'),
				Field('user_email'),
				Field('product_id', 'reference product'),
                Field('review_time', 'datetime', default=get_current_time()),
				)

db.define_table('stars',
				Field('user_email'),
				Field('product_id', 'reference product'),
				Field('rating', 'integer', default=0),
				)

db.define_table('shopping_cart',
				Field('user_email'),
				Field('product_id', 'reference product'),
				Field('quantity', 'integer', default=0),
				)
				

db.product.id.readable = False
db.product.id.writable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
