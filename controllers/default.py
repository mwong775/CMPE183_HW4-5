# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """Displays a list of products.  For the store owner, the list is editable.
    For customers, the list is not editable, but if products are in stock,
    there is a buy button."""
    # Fields to display.
    fields = [db.product.id, db.product.product_name, db.product.product_price]
    links = []
    if is_owner():
        # All products
        q = db.product
        # We want to see also the quantity in stock.
        fields.extend([db.product.product_quantity])
    else:
        # For other people, only those in stock.
        q = db.product.product_quantity > 0
        # If the user is a customer, we add a button to buy it.
        if is_customer():
            links.append(dict(
                header='', # This is the header in the table for the buttons; not needed here.
                body= lambda row : A(T('Buy'), _href=URL('default', 'buy', args=[row.id]), _class='btn')
            ))
    form = SQLFORM.grid(
        q,
        fields=fields,
        links=links,
        editable=is_owner(),
        deletable=is_owner(),
        csv=is_owner(),
        details=True,
    )
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


