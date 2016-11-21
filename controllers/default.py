# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# Sample shopping cart implementation.
# -------------------------------------------------------------------------

import traceback


def get_products():
    """Gets the list of products"""
    q = db.product.id > 0
    products = db(q).select(db.product.ALL)
    # Fixes some fields, to make it easy on the client side.
    return response.json(dict(
        products=products,
    ))


@auth.requires_login()
def index():
    if get_user_email() != 'luca@ucsc.edu':
        raise HTTP(403)
    q = db.product # This queries for all products.
    form = SQLFORM.grid(
        q,
        editable=True,
        create=True,
        user_signature=True,
        deletable=True,
        fields=[db.product.product_name, db.product.quantity, db.product.price,
                db.product.image_url],
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


