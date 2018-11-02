# Here go your api methods.

import time

@auth.requires_signature()
def get_title():
    u = get_user_email()
    t = db(db.my_table.the_user == u).select().first()
    return response.json(dict(title=t.the_title or ""))

@auth.requires_signature()
def set_title():
    u = get_user_email()
    db.my_table.update_or_insert(
        db.my_table.the_user == u,
        the_title = request.vars.title,
    )
    time.sleep(2)
    return "ok"
