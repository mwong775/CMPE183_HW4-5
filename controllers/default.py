# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime

class Post(object):
    """Simple class to create synthetic posts"""
    def __init__(self):
        pass

def attacker():
    """This controller simply produces the attack page for Form 1.
    The interesting bits are found in the corresponding view."""
    return dict()

def simple_index():
    """Unlike the real index, this does not take data from the database."""
    post1 = Post()
    post1.id = 1
    post1.post_title = "Synthetic post 1 title"
    post1.post_content = "Synthetic post 1 content"
    post1.post_author = "luca@ucsc.edu"
    post1.post_time = datetime.datetime.utcnow()
    post2 = Post()
    post2.id = 2
    post2.post_title = "Synthetic post 2 title"
    post2.post_content = "Synthetic post 2 content"
    post2.post_author = "luca@ucsc.edu"
    post2.post_time = datetime.datetime.utcnow()
    return dict(
        rows=[post1, post2]
    )


@auth.requires_login()
def setup():
    """Inserts a couple of posts just to bring the database to a known state.
    This is done for debugging purposes ony, and should not be part of a real web site."""
    db(db.post).delete() # Deletes the content of the post table.
    db.post.insert(post_title="First Post",
                   post_content="Content of first post")
    db.post.insert(post_title="Second Post",
                   post_content="Content of second post")
    # We don't need a view if we don't return a dictionary.
    return "ok"


def index():
    """Displays the list of rows"""
    rows = db(db.post).select()
    return dict(
        rows=rows,
    )


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

    # Here there is request.vars.post_title
    logger.info("type: %r" % type(request.vars.view_count))

    # For this controller only, we hide the author.
    db.post.post_author.readable = False

    # post = db(db.post.id == int(request.args[0])).select().first()

    post = db.post(request.args(0))
    # We must validate everything we receive.
    if post is None:
        logger.info("Invalid edit call")
        redirect(URL('default', 'index'))
    # One can edit only one's own posts.
    if post.post_author != auth.user.email:
        logger.info("Attempt to edit some one else's post by: %r" % auth.user.email)
        redirect(URL('default', 'index'))
    # Now we must generate a form that allows editing the post.
    form = SQLFORM(db.post, record=post)
    if form.process(onvalidation=mychecks).accepted:
        logger.info("The title is: %r" % form.vars.post_title)
        logger.info("Count: %d" % form.vars.view_count)
        # The deed is done.
        redirect(URL('default', 'index'))
    return dict(form=form)


def mychecks(form):
    """Performs form validation.  
    See http://www.web2py.com/books/default/chapter/29/07/forms-and-validators#onvalidation 
    for details."""
    # form.vars contains what the user put in.
    if form.vars.view_count % 2 == 1:
        form.errors.view_count = "I am sorry but it's odd that you wrote %d" % form.vars.view_count


def produce_funny_button(row):
    if 'user' in row.post_title:
        return A(I(_class='fa fa-eye'), ' ', 'View user post', 
                    _href=URL('default', 'view_in_grid', args=[row.id], user_signature=True),
                    _class='btn')
    else:
        return SPAN(auth.user.email if auth.user is not None else 'bleh', _class='red')


def viewall():
    """This controller uses a grid to display all posts."""
    # I like to define the query separately.
    query = db.post

    # List of additional links.
    links = []
    links.append(
        dict(header='',
             body = lambda row : 
             SPAN(A(I(_class='fa fa-eye'), ' ', 'View', 
                    _href=URL('default', 'view_in_grid', args=[row.id], user_signature=True),
                    _class='btn'),
                _class="haha")
        )
    )

    links.append(
        dict(header='',
             body = lambda row : 
             SPAN(A(I(_class='fa fa-eye'), ' ', 'View', 
                    _href=URL('default', 'view_in_grid_v', vars=dict(id=row.id), user_signature=True),
                    _class='btn'),
                _class="haha")
        )
    )

    links.append(
        dict(header='',
             body = lambda row : 
             SPAN(A('Edit', 
                    _href=URL('default', 'edit', args=[row.id], user_signature=True),
                    _class='btn'),
                _class="haha")
        )
    )
    links.append(
        dict(header = "Optional",
            body = produce_funny_button # lambda row : produce_funny_button(row)
        )
    )

    links.append(
        dict(header="Rightback", body = lambda row : A('rb', _class='btn', 
            _href=URL('default', 'rightback', args=[row.id], 
                        vars= {} if request.vars.page is None else dict(page=request.vars.page),
                        user_signature=True)))
    )

    # Let's get rid of some fields in the add form.
    # Are we in the add form?
    if len(request.args) > 0 and request.args[0] == 'new':
        db.post.post_author.readable = False
        db.post.post_time.readable = False

    # Grid definition.
    grid = SQLFORM.grid(
        query, 
        field_id = db.post.id, # Useful, not mandatory.
        fields = [db.post.id, db.post.post_title, db.post.view_count,
                    db.post.post_author, db.post.post_time], 
        links = links,
        # And now some generic defaults.
        details=False,
        create=True, editable=False, deletable=False,
        csv=True, 
        paginate=2,
        user_signature=True, # We don't need it as one cannot take actions directly from the form.
    )
    return dict(grid=grid)


@auth.requires_signature()
def rightback():
    post = db.post(request.args(0))
    if post is None:
        redirect(URL('default', 'index'))
    post.view_count = 1 if post.view_count is None else post.view_count + 1
    post.update_record()
    if request.vars.page is not None:
        return redirect(URL('default', 'viewall', vars=dict(page=request.vars.page)))
    else:
        return redirect(URL('default', 'viewall'))


@auth.requires_signature()
def view_in_grid():
    post = db.post(request.args(0))
    if post is None:
        redirect(URL('default', 'index'))
    post.view_count = 1 if post.view_count is None else post.view_count + 1
    form = SQLFORM(db.post, record = post, readonly=True)
    post.update_record()
    return dict(form=form)

@auth.requires_signature()
def view_in_grid_v():
    post = db.post(request.vars.id)
    if post is None:
        redirect(URL('default', 'index'))
    form = SQLFORM(db.post, record = post, readonly=True)
    return dict(form=form)




def view1():
    post = db.post(request.args(0))
    if post is None:
        redirect(URL('default', 'index'))
    form = SQLFORM(db.post, record = post, readonly=True)
    return dict(form=form)


def view2():
    post = db.post(request.args(0))
    return dict(post=post)


def urls():
    # request.args[1]
    # request.vars.person
    return dict()


# /start/default/delete/2
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
    redirect(URL('default', 'index_inefficient'))



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


