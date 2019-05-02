# Here go your api methods.


@auth.requires_signature()
def add_post():
    """Adds a post."""
    db.post.insert(
        post_title=request.vars.post_title,
        post_content=request.vars.post_content,
    )
    return("ok") # We could also return something else, but this will be good enough.

