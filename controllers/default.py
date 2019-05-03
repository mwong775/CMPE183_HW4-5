# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    grid = SQLFORM.grid(db.product,
        create=True, editable=True, 
    )
    return dict(grid=grid)


def store():
    """Returns the store page, with the list of products to be bought"""
    # Complete.
    return dict()


@auth.requires_login()
def create_order():
    """Page to create an order, accessed from the Buy button."""
    product = db.product(request.args(0))
    profile = db(db.profile.email == auth.user.email).select().first()
    if profile is None:
        redirect(URL('default', 'profile',
                     vars=dict(next=URL('default', 'create_order', args=[product.id]),
                               edit='y')))
    # Ok, here you know the profile exists.
    # Sets the default for the order to be created. 
    db.orders.product_id.default = product.id
    db.orders.user.default = auth.user.email
    db.orders.order_date.default = datetime.datetime.utcnow()
    # Complete.  You have to create a form for inserting an order, and process/return it. 
    return dict()


@auth.requires_login()
def profile():
    """Page for creating/editing/viewing a profile. 
    It has two modes: edit/create, and view."""
    # This is the email of the user to which the form applies.
    user_email = request.vars.email or auth.user.email
    if request.vars.edit == 'y':
        # Mode for create/edit. 
        # You need to create a form to create (if there is no profile)
        # or edit (if there is a profile) the profile for the user.
        form = None # Placeholder.  
        if form.process().accepted:
            redirect(request.vars.next or URL('default', 'index'))

    else:
        # Mode for view.
        # You need to read the profile for the user, and return a view form for it, 
        # generated with SQLFORM(db.profile, profile, readonly=True). 
        # You do not need to process the form.
        form = None # Placeholder.  
    return dict(form=form)


@auth.requires_login()
def order_list():
    """Page to display the list of orders."""
    # Fixes visualization of email and product.  I hope this works, it should give you the idea at least.
    db.product_order.user_email.represent = lambda v, r : A(v, _href=URL('default', 'profile', vars=dict(email=v)))
    db.product_order.product_id.represent = lambda v, r : A(get_product_name(db.product(v)), _href=URL('default', 'view_product', args=[v]))
    grid = SQLFORM.grid(db.product_order,
        # Complete if needed.
    )
    return dict(grid=grid)


def view_product():
    """Controller to view a product."""
    p = db.product(request.args(0))
    if p is None:
        form = P('No such product')
    else:
        form = SQLFORM(db.product, p, readonly=True)
    return dict(form=form)


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


