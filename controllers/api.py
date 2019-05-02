# Here go your api methods.


@auth.requires_signature()
def add_post():
    """Adds a post."""
    db.post.insert(
        form_title=request.vars.form_title,
        form_content=request.vars.form_content,
    )
    return("ok") # We could also return something else, but this will be good enough.

