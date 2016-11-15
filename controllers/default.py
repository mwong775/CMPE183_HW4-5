# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import json
import random

def index():
    return dict()


def get_initial_board(_):
    symbol = random.choice(['x', 'o'])
    return dict(
        board = [''] * 9,
        turn = symbol,
        playing = [symbol],
        youare = symbol,
    )


def get_state():
    """
    ?p=yadayada
     where yadayada is the token that the two players have in common.
    """
    if not request.vars.p:
        raise HTTP(500)
    r = db(db.board.game_token == request.vars.p).select().first()
    if r is None:
        # First player.
        b = get_initial_board(None)
        db.board.insert(game_token = request.vars.p, game_state = json.dumps(b))
        # Marks in the user session that they are playing this role in this game.
        session.symbol = json.dumps([request.vars.p, b['youare']])
    else:
        b = json.loads(r.game_state)
        if len(b['playing']) == 1:
            # Second player.
            symbol = 'x' if 'o' in b['playing'] else 'o'
            session.symbol = json.dumps([request.vars.p, symbol])
            b['youare'] = symbol
            b['playing'] = ['x', 'o']
            r.update_record(game_state = json.dumps(b))
        else:
            # Both are already playing, just give back the board state.
            pass
    return response.json(dict(state=b))


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


