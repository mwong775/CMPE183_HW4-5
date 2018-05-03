# Here go your api methods.


@auth.requires_signature()
def edit():
    logger.info("The user has set a new value: %r" % request.vars.my_string)
    return "ok"