# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import json

from gluon.utils import web2py_uuid

def index():
    """
    I am not doing anything here.  Look elsewhere.
    """
    return dict()


def get_products():
    """Gets the list of products, possibly in response to a query."""
    t = request.vars.q.strip()
    if request.vars.q:
        q = ((db.product.name.contains(t)) |
             (db.product.description.contains(t)))
    else:
        q = db.product.id > 0
    products = db(q).select(db.product.ALL)
    # Fixes some fields, to make it easy on the client side.
    for p in products:
        p.image_url = URL('download', p.image)
        p.desired_quantity = min(1, p.quantity)
        p.cart_quantity = 0
    return response.json(dict(
        products=products,
    ))

def create_order():
    """Creates an order (AJAX function)"""
    cart = request.vars.cart
    # Stores the cart, and creates an order number.
    # It would be better to randomize the order number, but here for simplicity we don't.
    order_key = web2py_uuid()
    order_id = db.product_order.insert(cart=cart, order_key=order_key)
    return response.json(dict(order_id=order_id, order_key=order_key))

def pay_order():
    """Pays with stripe"""
    order_id = request.vars.order_id
    order = db.product_order(order_id)
    logger.info("Order is: %r", order)
    cart = json.loads(order.cart)
    total = 0
    for p in cart:
        total += p['cart_quantity'] * p['price']
    return dict(order_id=order_id, order_key=order.order_key, cart=cart, total=total * 100)

def order_paid():
    """Payment confirmation from stripe."""
    order_id = request.args(1)
    order_key = request.args(2)
    order = db.product_order(order_id)
    if order.order_key == order_key:
        order.update_record(paid=True)
        logger.info("Order is paid: %r", order)
        return "ok"
    raise HTTP(500)

def get_cart():
    return response.json(dict(cart=session.cart or []))

def post_cart():
    session.cart = json.loads(request.vars.cart)

# Normally here we would check that the user is an admin, and do programmatic
# APIs to add and remove products to the inventory, etc.
@auth.requires_login()
def product_management():
    q = db.product # This queries for all products.
    form = SQLFORM.grid(
        q,
        editable=True,
        create=True,
        user_signature=True,
        deletable=True,
        fields=[db.product.product_name, db.product.quantity, db.product.price,
                db.product.image],
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


