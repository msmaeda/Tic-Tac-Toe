from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
from engine import board
from engine.board import GameState
from engine.bot import botMove

def new(request):
    """ Handles new requests for games """
    gs              = GameState()
    state           = gs.reset()
    return render_to_response("board.html", { 'state' : state, 'info_message' : 'Your Move First'})

def move(request,position,state):
    """ Handles player move """
    gs              = GameState()
    sGameState      = str(state)
    iGameState      = []
    response_dict   = {}

    for ci in sGameState:
        if int(ci) == 2:
            iGameState.append(board.COMPUTER_PLAYER)
        else:
            iGameState.append(int(ci))

    newState        = gs.move(board.HUMAN_PLAYER,iGameState,int(position))

    if newState is None:
        response_dict.update({'status' : 'err', 'msg' : 'Invalid move'})
    elif gs.isGameOver(newState):
        winner      = gs.getWinner(newState)

        if winner is None:
            response_dict.update({'status'  : 'gameover',
                                  'msg'     : 'Tie Game',
                                  'state'   : newState})
        elif winner == board.HUMAN_PLAYER:
            response_dict.update({'status'  : 'gameover', 
                                  'msg'     : 'Player Wins!',
                                  'state'   : newState})
        else:
            response_dict.update({'status'  : 'gameover', 
                                  'msg'     : 'Computer Wins!',
                                  'state'   : newState})
    else:
        aiMove      = botMove(newState)

        if aiMove is None:
            response_dict.update({'status'  : 'err', 
                                  'msg'     : 'Something has gone wrong'})
        else:
            fState  = gs.move(board.COMPUTER_PLAYER,newState,aiMove)

            if gs.isGameOver(fState):
                response_dict.update({'status'  : 'gameover', 
                                      'msg'     : 'Computer Wins!',
                                      'state'   : fState})
            else:
                response_dict.update({'status'  : 'ok', 
                                      'msg'     : 'Your move',
                                      'state'   : fState})

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
