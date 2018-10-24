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

# Am I the owner of the store, or a customer?
def is_owner():
    return get_user_email() == 'seller@ucsc.edu'

def is_customer():
    return not is_owner()


db.define_table('product',
                Field('product_name'),
                Field('product_quantity', 'integer', ),
                Field('product_price', 'float'),
                Field('product_description', 'text'),
                )

# Validators
db.product.product_name.requires = IS_NOT_EMPTY()
db.product.product_quantity.requires = IS_INT_IN_RANGE(0, None)
db.product.product_price.requires = IS_FLOAT_IN_RANGE(0, None)

# Visibility
db.product.id.readable = db.product.id.writable = False

# Labeling in forms etc
db.product.product_quantity.label = 'Quantity'
db.product.product_price.label = 'Price'
db.product.product_description.label = 'Description'

db.define_table('product_order',
                Field('product_ordered', 'reference product'),
                Field('quantity', 'integer'),
                Field('shipping_method'),
                Field('customer', default=get_user_email()),
                Field('order_time', default=datetime.datetime.utcnow())
                )

# Validators
# The ones below also generates the drop down lists.
db.product_order.product_ordered.requires = IS_IN_DB(db, db.product.id, '%(product_name)s')
db.product_order.shipping_method.requires = IS_IN_SET(['Air', 'Surface', 'Underground'])
# This one is just a positive range validator.
db.product_order.quantity.requires = IS_INT_IN_RANGE(0, None)



# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
