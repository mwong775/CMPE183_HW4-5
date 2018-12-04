# Note that we require login in these forms, so non-logged-in users
# cannot add data.

@auth.requires_login()
def strong_form():
    form = SQLFORM(db.mytable)
    if form.process().accepted:
        redirect(URL('default', 'index'))
    return dict(form=form)

@auth.requires_login()
def weak_form():
    if request.post_vars:
        # Inserts the data.
        db.mytable.insert(
            title=request.vars.title,
            paragraph=request.vars.paragraph,
            quantity=int(request.vars.quantity)
        )
        redirect(URL('default', 'index'))
    return dict()
