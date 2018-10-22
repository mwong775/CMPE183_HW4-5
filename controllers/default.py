# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime


def index_with_many_queries():
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


def index():
    result = [] # We will accummulate the result here.
    if auth.user is None:
        # We cannot give information on stars; we can simply give out a list of posts.
        for r in db(db.post.id > 0).select():
            result.append(dict(
                post_title=r.post_title,
                post_author=r.post_author,
                post_content=r.post_content,
                starred=False, # The button bar in any case should not be displayed if one is not logged in.
                id=r.id,
            ))
    else:
        # The user is logged in.  In this case, we can pull out of the db also the stars.
        # To understand this version of the code, please see
        # http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#One-to-many-relation
        # We are doing a "left outer join", because some posts may not be starred.
        rows = db().select(db.post.ALL, db.star.ALL,
                           left=db.star.on(
                               (db.post.id == db.star.post_id) & # The star has to be for the post
                               (db.star.user_id == auth.user.id) # And it must be from the logged in user.
                           ))

        for r in rows:
            # Notice that here we avoid doing one query for each row.
            # We already know whether things are starred or not.
            result.append(dict(
                post_title=r.post.post_title, # Notice how we have to say r.post.post_title rather than r.post_title.
                post_author=r.post.post_author,
                post_content=r.post.post_content,
                starred=r.star.id is not None, # It does not matter here which field of star we check for existence.
                id=r.post.id, # This is the id of the post, as before.
            ))
    logger.info("Result: %r" % result)
    return dict(rows=result)


def index_thumbs():
    result = [] # We will accummulate the result here.
    num_posts = 2
    try:
        num_posts = int(request.vars.num_posts)
    except ValueError:
        pass
    if auth.user is None:
        # We cannot give information on stars; we can simply give out a list of posts.
        for r in db(db.post.id > 0).select():
            result.append(dict(
                post_title=r.post_title,
                post_author=r.post_author,
                post_content=r.post_content,
                starred=False, # The button bar in any case should not be displayed if one is not logged in.
                id=r.id,
            ))
    else:
        # The user is logged in.  In this case, we can pull out of the db also the stars.
        # To understand this version of the code, please see
        # http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#One-to-many-relation
        # We are doing a "left outer join", because some posts may not be starred.
        rows = db().select(db.post.ALL, db.star.ALL,
                           left=db.star.on(
                               (db.post.id == db.star.post_id) & # The star has to be for the post
                               (db.star.user_id == auth.user.id) # And it must be from the logged in user.
                           ), limitby=(0, num_posts), orderby=db.post.post_time)
        for r in rows:
            # I need to get from the DB two additional things.
            # First, I want the list of people who thumbed it up/down.
            # Then, I also want to know if I (the logged in user) thumbed it up/down.
            thumb_rows = db(db.thumb.post_id == r.post.id).select()
            thumb_ups = []
            thumb_downs = []
            my_thumb = None
            for thumb_row in thumb_rows:
                # I am iterating on the thumbings for this particular post.
                if thumb_row.thumb_state == 'u':
                    thumb_ups.append(thumb_row.user_email)
                elif thumb_row.thumb_state == 'd':
                    thumb_downs.append(thumb_row.user_email)
                if thumb_row.user_email == auth.user.email:
                    my_thumb = thumb_row.thumb_state
            # Notice that here we avoid doing one query for each row.
            # We already know whether things are starred or not.
            result.append(dict(
                post_title=r.post.post_title, # Notice how we have to say r.post.post_title rather than r.post_title.
                post_author=r.post.post_author,
                post_content=r.post.post_content,
                starred=r.star.id is not None, # It does not matter here which field of star we check for existence.
                liked=thumb_ups,
                disliked=thumb_downs,
                my_thumb=my_thumb,
                id=r.post.id, # This is the id of the post, as before.
            ))
    logger.info("Result: %r" % result)
    return dict(rows=result, num_posts=num_posts)


@auth.requires_signature()
@auth.requires_login()
def thumb():
    post_id = int(request.args[0])
    # Let's use the "update_or_insert" database method, so our code will be more compact.
    # See http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#update_or_insert
    db.thumb.update_or_insert(
        (db.thumb.post_id == post_id) & (db.thumb.user_email == auth.user.email), # Query
        post_id=post_id, # And fields.
        user_email=auth.user.email,
        thumb_state=request.args[1]
    )
    # That's it; the deed is done.
    redirect(request.vars.next)


@auth.requires_signature()
@auth.requires_login()
def thumb_unthumb():
    """In this version of the code, clicking on an already clicked thumb deletes it."""
    post_id = int(request.args[0])
    thumb_record = db((db.thumb.post_id == int(request.args[0])) &
                      (db.thumb.user_email == auth.user.email)).select().first()
    new_state = request.args[1]
    if thumb_record is None:
        # We insert the new state.
        db.thumb.insert(
            user_email=auth.user.email,
            post_id=post_id,
            thumb_state=new_state,
        )
    else:
        if thumb_record.thumb_state == new_state:
            # Two clicks deletes the thumb. For delete_record, see
            # See http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#select
            thumb_record.delete_record()
        else:
            # We update the record;
            # see http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#update_record
            thumb_record.update_record(thumb_state=new_state)
    # That's it; the deed is done.
    redirect(request.vars.next)


@auth.requires_signature()
@auth.requires_login()
def toggle_star():
    star_record = db((db.star.post_id == int(request.args[0])) &
        (db.star.user_id == auth.user_id)).select().first()
    if star_record is not None:
        # Removes star.
        db(db.star.id == star_record.id).delete()
    else:
        # Adds the star.
        db.star.insert(
            user_id = auth.user.id,
            post_id = int(request.args[0]))
    redirect(request.vars.next) # Notice that now it's the request that tells us where to go next.


def please_no_q(form):
    """This is a function, not a controller, as it has one argument."""
    if 'q' in form.vars.post_title:
        form.errors.post_title = "You wrote the terrible letter in the title! This is not allowed."
    if 'q' in form.vars.post_content:
        form.vars.post_title += ' ' + "Warning: the post content contains the Letter That Shall Not Be Written"


@auth.requires_login()
def add2():
    """More sophisticated way, in which we use web2py to come up with the form."""
    form = SQLFORM.factory(
        Field('post_title'),
        Field('post_content', 'text'),
    )
    # We can process the form.  This will check that the request is a POST,
    # and also perform validation, but in this case there is no validation.
    if form.process(onvalidation=please_no_q).accepted:
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


