# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

# Violates first normal form.

db.define_table('address',
    Field('first_name'),
    Field('last_name'),
    Field('phones', 'text'),
)

# Example: 
db.address.insert(
    first_name = "Luca",
    last_name = "de Alfaro",
    phones = json.dumps(lucaphonelist)
)

for row in db(db.address.first_name == 'Luca').select()
    print row.first_name
    print json.loads(row.phones)

# In first normal form. 

db.define_table('address',
    Field('first_name'),
    Field('last_name'),
)

db.define_table('phone',
    Field('address_id', 'reference address') # FOREIGN KEY This will contain the id of the addresses row.
    Field('phone_type'),
    Field('number'),
)

# What are Luca's phones? 
for row in db((db.address.first_name == 'Luca') & 
              (db.phone.address_id == db.address.id)).select():

    print row.address.first_name
    print row.phone.number


for row in db(db.address.first_name == 'Luca').select():
    print "For", row.first_name, "I have these numbers:"
    for arow in db(db.phone.address_id == row.id).select():
        print "  ", arow.phone_type, ":", arow.number

# Create a new entry for Ugo with 1234 as mobile. 
uid = db.address.insert(first_name='Ugo', last_name='de Alfaro')
db.phone.insert(address_id = uid, number="1234")

# Add the number for Luca home as 1357:
row = db((db.address.first_name == "Luca") & (db.address.last_name == "de Alfaro")).select().first()
if row is not None:
    db.phone.insert(address_id = row.id, number="1357")
else:
    # I need to do insert also of the address as above. 


# Delete all Maria's info: 
db(db.address.name == "Maria").delete()


# Students and classes

db.define_table('student',
    Field('name'),
    Field('good_standing', 'boolean'),
)

db.define_table('ucclass',
    Field('name'),
)

db.define_table('enrolled',
    Field('student_id', 'reference student'),
    Field('class_id', 'reference ucclass'),
    Field('enrollment_date', 'datetime'),
)

for row in db(
                (db.student.name == 'Luca') &
                (db.student.id == db.enrolled.student_id) &
                (db.ucclass.id == db.enrolled.class_id) 
             ).select():
    print "Luca is in", row.ucclass.name
    


# For Luca I have these numbers:
#     Mobile: 1234
#     Office: 5678


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# Inventing crowdgrader. 
def get_email():
    return None if auth.user is None else auth.user.email

db.define_table('submission', 
    Field('student', 'reference auth.user'), # way 1, via id of table auth.user
    Field('student', default=get_email())    # way 2, via email.

)