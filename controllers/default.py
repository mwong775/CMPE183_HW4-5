# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    form = SQLFORM.factory(
        Field('ingr1', label=T('First ingredient'), default='Garlic'),
        Field('ingr2', label='Second ingredient')
    )
    if form.process().accepted:
        db.compatible.insert(
            ingredient1 = form.vars.ingr1.lower(),
            ingredient2 = form.vars.ingr2.lower()
        )
        redirect(URL('default', 'index'))
    return dict(form=form)


def put_lowercase(row_id):
    return A(
        'Make lowercase',
        _href=URL('default', 'tolower', args=[row_id]),
        _class='btn rounded orange',
    )

def tolower():
    row = db.compatible(request.args(0))
    if row is not None:
        row.ingredient1 = row.ingredient1.lower()
        row.ingredient2 = row.ingredient2.lower()
        row.update_record()
    redirect(URL('default', 'view'))


def view():
    q = (db.compatible.id > 0)
    # q = (db.compatible.ingredient1 == "Garlic")
    grid = SQLFORM.grid(q,
        fields=[db.compatible.ingredient1, db.compatible.ingredient2],
        details = False,
        csv=False, create=True, editable=True, deletable=False, searchable=True,
        links=[lambda r: put_lowercase(r.id)],
        sortable=True,
        maxtextlength=24,
        )
    return dict(grid=grid)



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


