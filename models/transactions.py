# Methods to manage db transactions.

# This depends on database type.

import traceback, gluon

class Transaction(object):

    def __init__(self, always=False):
        self.db_type = myconf.get('db.uri').split(':')[0]
        self.always = always

    def __enter__(self):
        if self.always or request.env.request_method == 'POST':
            db.commit()
            if self.db_type == 'mysql':
                db.executesql('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;')
            elif self.db_type == 'sqlite':
                db.executesql('PRAGMA locking_mode = EXCLUSIVE;')
                db.executesql('BEGIN EXCLUSIVE;')

    def __exit__(self, exc_type, exc_value, in_traceback):
        logger.info("exc_type: %r", exc_type)
        logger.info("exc_value: %r", exc_value)
        if exc_type is None or exc_type == gluon.http.HTTP:
            # Normal exit, we commit.
            try:
                db.commit()
            except:
                db.rollback()
                raise(HTTP(500))
        else:
            logger.error("Error: %s" % traceback.format_exc())
            db.rollback()
            raise(HTTP(500))
