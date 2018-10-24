# Methods to manage db transactions.

# This depends on database type.

db_type = myconf.get('db.uri').split(':')[0]

def begin_serializable(always=False):
    if always or request.env.request_method == 'POST':
        db.commit()
        if db_type == 'mysql':
            db.executesql('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;')
        elif db_type == 'sqlite':
            db.executesql('PRAGMA locking_mode = EXCLUSIVE;')
            db.executesql('BEGIN EXCLUSIVE;')

def end_serializable():
    db.commit()
