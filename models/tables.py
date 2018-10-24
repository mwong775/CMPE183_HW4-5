# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('product',
                Field('product_name'),
                Field('product_quantity', 'integer', ),
                Field('quantity_ordered', 'integer', default=0),
                Field('product_price', 'float'),
                Field('product_description', 'text'),
                )

# Virtual fields. These are computed automatically for every record read.
db.product.in_stock = Field.Virtual('in_stock', lambda row: row.product.product_quantity - row.product.quantity_ordered)

# Validators
db.product.product_name.requires = IS_NOT_EMPTY()
db.product.product_quantity.requires = IS_INT_IN_RANGE(0, None)
db.product.product_price.requires = IS_FLOAT_IN_RANGE(0, None)

# Visibility
db.product.id.readable = db.product.id.writable = False
db.product.quantity_ordered.writable = False

# Labeling in forms etc
db.product.product_quantity.label = 'Quantity'
db.product.product_price.label = 'Price'
db.product.product_description.label = 'Description'
db.product.quantity_ordered.label = 'Total on order'

db.define_table('customer_order',
                Field('product_ordered', 'reference product'),
                Field('quantity', 'integer'),
                Field('shipping_method'),
                Field('customer', default=get_user_email()),
                Field('order_time', default=datetime.datetime.utcnow())
                )

# Validators
# The ones below also generates the drop down lists.
db.customer_order.product_ordered.requires = IS_IN_DB(db, db.product.id, '%(product_name)s')
db.customer_order.shipping_method.requires = IS_IN_SET(['Air', 'Surface', 'Underground'], zero=None)
db.customer_order.shipping_method.default = 'Surface'

# Labels
db.customer_order.product_ordered.label = T('Product')

# Visibility
db.customer_order.product_ordered.readable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
