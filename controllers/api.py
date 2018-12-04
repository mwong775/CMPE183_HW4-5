# Here go your api methods.

@auth.requires_login()
def insert_record():
    db.mytable.insert(
        title=request.vars.title,
        paragraph=request.vars.paragraph,
        quantity=int(request.vars.quantity)
    )
    return "ok"

@auth.requires_signature()
def insert_signed_record():
    db.mytable.insert(
        title=request.vars.title,
        paragraph=request.vars.paragraph,
        quantity=int(request.vars.quantity)
    )
    return "ok"

