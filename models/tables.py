# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


DATE_FORMAT = '%Y-%m-%d %H:%M %Z'
datetime_validator = IS_LOCALIZED_DATETIME(timezone=pytz.timezone(user_timezone), format=DATE_FORMAT)
FULL_DATE_FORMAT = '%Y-%m-%d %H:%M:%S %Z'
full_datetime_validator = IS_LOCALIZED_DATETIME(timezone=pytz.timezone(user_timezone), format=FULL_DATE_FORMAT)

db.define_table('example_table',
                Field('entry_name'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()))

db.example_table.created_on.requires = datetime_validator

# nice_string = datetime_validator.formatter(utc_string)
# utc_string, error_msg = datetime_validator(nice_string)

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
