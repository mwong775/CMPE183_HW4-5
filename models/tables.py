# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

db.define_table(
    'board',
    Field('game_token'),
    Field('game_state', 'text'), # Json-encoded game state.
)


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


# Let us decode the session.
import json
tictactoe_dict = {} if session.tictactoe is None else json.loads(session.tictactoe)