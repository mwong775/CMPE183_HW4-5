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
        fields.extend([db.product.product_quantity, db.product.quantity_ordered])
        # We cannot add virtual fields to fields, so we have to represent this as a link.
        links.append(dict(header='In stock',
                          body= lambda row : row.product_quantity - row.quantity_ordered))
    else:
        # For other people, only those in stock.
        q = db.product.product_quantity > db.product.quantity_ordered
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

def validate_purchase(product):
    """We need to check that we have enough in stock.
    We need to do this when processing the form, since things could have changed (others might
    have bought stuff) since we produced the form.
    More in detail, when you produce the form, we know that the product is in stock.
    But before the user makes up their mind and submits the form, someone else might have bought
    the stuff in another transaction.

    A validator, as passed to the form.process() onvalidate argument, is a function
    that takes ONLY a form as argument.  And the form does not contain the product price.
    So what I do is this.  The function check_total_price gets as argument the product
    of the product, and returns the validator function itself, that gets the form as
    its argument."""
    def f(form):
        """This is the actual validator."""
        in_stock = product.product_quantity - product.quantity_ordered
        if form.vars.quantity > in_stock:
            form.errors.quantity = T('I am sorry; I have only %d in stock' % in_stock)
    # I return the validator function
    return f


@auth.requires_login()
def buy():
    """Allows customers to buy stuff."""
    product = db.product(request.args(0))
    if product is None:
        # No such product found.
        redirect(URL('default', 'index'))
    stock_amount = product.product_quantity - product.quantity_ordered
    if stock_amount <= 0:
        # Not in stock.
        session.message = T("The product is not in stock")
        redirect(URL('default', 'index'))
    # Okkay, we have the product.  Let's produce a form.
    # Customizations for the form.
    db.customer_order.product_ordered.readable = db.customer_order.product_ordered.writable = False
    db.customer_order.customer.readable = db.customer_order.customer.writable = False
    db.customer_order.order_time.readable = db.customer_order.order_time.writable = False
    # I can create the form now.
    form = SQLFORM(db.customer_order)
    # I pre-fill that the order is for socks.
    form.vars.product_ordered = int(request.args(0))
    # If there is a variable indicating the quantity, we use it to initialize it.
    # Otherwise, we initalize the quantity of the order to 1.
    if request.vars.q is None:
        form.vars.quantity = 1
    else:
        form.vars.quantity = min(stock_amount, int(request.vars.q))
    # Form processing.
    # If this is a POST, we need to do a database transaction.
    with Transaction():
        if form.process(onvalidation=validate_purchase(product)).accepted:
            # We have to update the quantity ordered.
            product.update_record(quantity_ordered = product.quantity_ordered + form.vars.quantity)
            session.flash = T('The order has been placed.  Thank you for your business.')
            redirect(URL('default', 'index'))
    return dict(name=product.product_name, form=form)


@auth.requires_login()
def orders():
    """Displays orders.  If we are the shop owner, this will display all orders,
    otherwise, it will just display our own orders."""
    # Fields to display.
    fields = [db.customer_order.id, db.product.product_name,
              db.customer_order.product_ordered, # This is needed for the join even if we don't show it.
              db.customer_order.quantity,
              db.product.product_price, db.product.id, ]
    links = []
    if is_owner():
        # All products
        q = (db.customer_order.product_ordered == db.product.id)
        # We want to see also the quantity in stock.
        fields.extend([db.product.product_quantity, db.product.quantity_ordered, db.customer_order.customer])
        db.customer_order.customer.readable = True
        db.customer_order.quantity.label = 'Order quantity' # To disambiguate.
        db.product.product_quantity.label = 'Quantity in stock'
    else:
        # For other people, only their own orders.
        db.customer_order.id.readable = False
        q = ((db.customer_order.product_ordered == db.product.id) & # This joins the tables.
             (db.customer_order.customer == get_user_email())) # Ordered by me.
        # If the user is a customer, we add a button to reorder it it.
        links.append(dict(
            header='', # This is the header in the table for the buttons; not needed here.
            body= lambda row : A(
                T('Reorder'),
                _href=URL('default', 'buy',
                          args=[row.product.id],
                          vars=dict(q=row.customer_order.quantity)),
                _class='btn')
        ))
    # There is also a link to delete an order.
    links.append(dict(
        header='',
        body = lambda row : A(
            T('Cancel Order'),
            _href=URL('default', 'cancel_order',
                      args=[row.customer_order.id],
                      vars=dict(next=URL(args=request.args, vars=request.get_vars)), # Go back here
                      user_signature=True),
            _class='btn'
        )
    ))
    form = SQLFORM.grid(
        q,
        fields=fields,
        links=links,
        editable=False,
        deletable=False,
        csv=is_owner(),
        details=False, # Does not work well for joins.
    )
    return dict(form=form)


@auth.requires_signature()
def cancel_order():
    """Cancels an order."""
    order = db.customer_order(request.args(0))
    if order is None:
        redirect(URL('default', 'index'))
    # We decrement the quantity on order.
    product = db.product(order.product_ordered)
    if product is None:
        redirect(URL('default', 'index'))
    with Transaction():
        product.update_record(quantity_ordered = product.quantity_ordered - order.quantity)
        order.delete_record()
    redirect(request.vars.next)


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


