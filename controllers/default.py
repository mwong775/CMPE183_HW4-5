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

def check_total_price(price):
    """I want to check that what the customer orders is not over $100.
    A validator, as passed to the form.process() onvalidate argument, is a function
    that takes ONLY a form as argument.  And the form does not contain the product price.
    So what I do is this.  The function check_total_price gets as argument the price
    of the product, and returns the validator function itself, that gets the form as
    its argument."""
    def f(form):
        """This is the actual validator."""
        if form.vars.quantiy * price > 100.:
            form.errors.quantity = T('Your order cannot be over $100')
    # I return the validator function
    return f

@auth.requires_login()
def buy():
    """Allows customers to buy stuff."""
    product = db.product(request.args(0))
    if product is None:
        # No such product found.
        redirect(URL('default', 'index'))
    if product.product_quantity <= 0:
        # Not in stock.
        session.message = T("The product is not in stock")
        redirect(URL('default', 'index'))
    # Okkay, we have the product.  Let's produce a form.
    # First, I fix the validator, so that I let you buy only as much as I have in stock.
    # This one is just a positive range validator.
    db.customer_order.quantity.requires = IS_INT_IN_RANGE(
        1, product.product_quantity, error_message='Maximum in stock: %d' % product.product_quantity)
    # Customizations for the form.
    db.customer_order.product_ordered.readable = db.customer_order.product_ordered.writable = False
    db.customer_order.customer.readable = db.customer_order.customer.writable = False
    db.customer_order.order_time.readable = db.customer_order.order_time.writable = False
    # I can create the form now.
    form = SQLFORM(db.customer_order)
    # I pre-fill that the order is for socks.
    form.vars.product_ordered = int(request.args(0))
    if form.process(onvalidate=check_total_price(product.product_price)).accepted:
        session.flash = T('The order has been placed.  Thank you for your business.')
        redirect(URL('default', 'index'))
    return dict(name=product.product_name, form=form)


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


