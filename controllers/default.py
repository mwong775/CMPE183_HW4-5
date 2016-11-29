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


def get_initial_board(symbol):
    return dict(
        board = [''] * 9,
        turn = symbol,
        playing = [symbol], # Set of players who showed up already.
    )


def complement(symbol):
    return list({'x', 'o'} - {symbol})[0]

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
        symbol = random.choice(['x', 'o'])
        b = get_initial_board(symbol)
        db.board.insert(game_token = request.vars.p, game_state = json.dumps(b))
        # Marks in the user session that they are playing this role in this game.
        tictactoe_dict[request.vars.p] = symbol
        youare = symbol
        theyare = ''
    else:
        # The game has already begun.
        b = json.loads(r.game_state)
        logger.info("game state: %r" % b)
        if len(b['playing']) == 1:
            # There is one player already.
            # Is it you?
            youare = tictactoe_dict.get(request.vars.p)
            if youare is not None:
                # You are playing already.
                theyare = ''
            else:
                # You joined as the second player.
                theyare = b['playing'][0]
                symbol = 'x' if 'o' in b['playing'] else 'o'
                tictactoe_dict[request.vars.p] = symbol
                b['playing'] = ['x', 'o']
                r.update_record(game_state = json.dumps(b))
                youare = symbol
        else:
            # Both are already playing, just give back the board state, and whose turn it is.
            youare = tictactoe_dict.get(request.vars.p)
            # If you are no-one, please go away.
            if youare is None:
                raise HTTP(403, 'Not authorized')
            theyare = complement(youare)
    session.tictactoe = json.dumps(tictactoe_dict)
    return response.json(dict(state=b, youare=youare, theyare=theyare))


def set_state():
    """Post for new state."""
    # 1- the game exists.
    # 2- you are the player the session tells me you are
    # 3- The board differs from the board I have only by
    #    the addition of a single symbol, which is equal
    #    to who you say you are.
    # 4- It's your turn to play.
    if not request.vars.p:
        raise HTTP(500)
    r = db(db.board.game_token == request.vars.p).select().first()
    if r is None:
        raise HTTP(500)
    b = json.loads(r.game_state)
    # Let's compute the difference between the two boards.
    new_board = json.loads(request.vars.new_board)
    diff = None
    for i in range(9):
        if new_board[i] != '' and b['board'][i] == '':
            if diff is None:
                # First different symbol.
                diff = new_board[i]
            else:
                raise HTTP(500)
        elif new_board[i] != b['board'][i]:
            raise HTTP(500)
    if diff is None:
        # No change.
        return "ok"
    # Ok, only one symbol is different, and it is in diff.
    youare = tictactoe_dict.get(request.vars.p)
    if youare != diff:
        raise HTTP(500)
    # Check that the player who played has the turn.
    if b.get('turn') != diff:
        raise HTTP(500)
    # Complements the turn.
    b['turn'] = complement(b['turn'])
    # Updates the board.
    b['board'] = new_board
    r.update_record(game_state = json.dumps(b))
    return "ok"


def is_name_available():
    return db(db.board.game_token == request.vars.p).select.first() is None


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


