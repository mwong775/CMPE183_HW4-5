def can_do_thing_1(city, user_email=None):
    """This requires edit priviledge."""
    if user_email is None and auth.user:
        user_email = auth.user.email
    pr = db((db.priviledge.user_email == user_email) &
            (db.priviledge.city == city)).select().first()
    return pr.permission in ['admin', 'edit']

