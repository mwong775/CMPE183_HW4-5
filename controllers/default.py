# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """

    if session.c is None:
        session.c = 1
    else:
        session.c += 1

    rows = db(db.post.id > 0).select()



    return dict(
        message=T('Welcome to web2py!'),
        ctime=datetime.datetime.now().isoformat(),
        visit_count=session.c,
        rows=rows,
    )

def index_inefficient():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """

    if session.c is None:
        session.c = 1
    else:
        session.c += 1

    rows = db(db.post.id > 0).select()

    result = []
    for r in rows:
        starred = (False if auth.user is None else
            db((db.star.post_id == r.id) & (db.star.user_id == auth.user.id)).select().first() is not None)
        result.append(dict(
            post_title=r.post_title,
            post_author=r.post_author,
            post_content=r.post_content,
            starred=starred,
            id=r.id,
        ))
    logger.info("Result: %r" % result)
    return dict(rows=result)


@auth.requires_login()
def add1():
    """INSECURE -- form does not contain token -- do not use."""
    """Very simple way to insert records."""
    logger.info("Request method: %r", request.env.request_method)
    if request.env.request_method == 'POST':
        # This is a postback.  Insert the record.
        logger.info("We are inserting: title: %r content: %r" % (
            # I could also access the title via request.post_vars.post_title,
            # but I don't care to differentiate betw post and get variables.
            request.vars.post_title, request.vars.post_content
        ))
        db.post.insert(
            post_title=request.vars.post_title,
            post_content=request.vars.post_content
        )
        redirect(URL('default', 'index'))
    else:
        # This is a GET request.  Returns the form.
        return dict()


@auth.requires_login()
def add2():
    """More sophisticated way, in which we use web2py to come up with the form."""
    form = SQLFORM.factory(
        Field('post_title'),
        Field('post_content', 'text'),
    )
    # We can process the form.  This will check that the request is a POST,
    # and also perform validation, but in this case there is no validation.
    if form.process().accepted:
        # We insert the result, as in add1.
        db.post.insert(
            post_title=form.vars.post_title,
            post_content=form.vars.post_content
        )
        # And we load default/index via redirect.
        redirect(URL('default', 'index'))
    # We ask web2py to lay out the form for us.
    logger.info("My session is: %r" % session)
    return dict(form=form)


@auth.requires_login()
def add3():
    """More sophisticated way, in which we use web2py to come up with the form."""
    form = SQLFORM(db.post)
    # We can process the form.  This will check that the request is a POST,
    # and also perform validation, but in this case there is no validation.
    # THIS process() also inserts.
    if form.process().accepted:
        # NOT NEEDED We insert the result, as in add1.
        # db.post.insert(
        #     post_title=form.vars.post_title,
        #     post_content=form.vars.post_content
        # )
        # And we load default/index via redirect.
        redirect(URL('default', 'index'))
    # We ask web2py to lay out the form for us.
    logger.info("My session is: %r" % session)
    return dict(form=form)


# We require login.
@auth.requires_login()
def edit():
    """Allows editing of a post.  URL form: /default/edit/<n> where n is the post id."""

    # if len(request.args) == 0:
    #     raise HTTP(500)
    # try:
    #     int_id = int(request.args[0])
    # except:
    #     raise HTTP(500)
    # rows = db(db.post.id == int_id).select()
    # for r in rows:
    #     post = r
    #     break
    # # Now we have post.

    # For this controller only, we hide the author.
    db.post.post_author.readable = False

    post = db.post(request.args(0))
    # We must validate everything we receive.
    if post is None:
        logging.info("Invalid edit call")
        redirect(URL('default', 'index'))
    # One can edit only one's own posts.
    if post.post_author != auth.user.email:
        logging.info("Attempt to edit some one else's post by: %r" % auth.user.email)
        redirect(URL('default', 'index'))
    # Now we must generate a form that allows editing the post.
    form = SQLFORM(db.post, record=post)
    if form.process().accepted:
        # The deed is done.
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_signature()
@auth.requires_login()
def delete():
    post = db.post(request.args(0))
    # We must validate everything we receive.
    if post is None:
        logging.info("Invalid edit call")
        redirect(URL('default', 'index'))
    # One can edit only one's own posts.
    if post.post_author != auth.user.email:
        logging.info("Attempt to edit some one else's post by: %r" % auth.user.email)
        redirect(URL('default', 'index'))
    db(db.post.id == post.id).delete()
    redirect(URL('default', 'index'))


# @auth.requires_login()
# def edit1():
#     post_id = request.vars.id # This matches the vars=dict(id=...) in index.html
#     post = db.post(post_id)
#     # We must validate everything we receive.
#     if post is None:
#         logging.info("Invalid edit call")
#         redirect(URL('default', 'index'))
#     form = SQLFORM.factory(
#         Field('post_title'),
#         Field('post_content', 'text'),
#     )




def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


