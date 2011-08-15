from django.test import TestCase
from engine import board
from engine.board import GameState

class GameStateTest(TestCase):
    """ Unit tests for game state """

    def test_reset(self):
        """ Tests new game """
        gs      = GameState()
        state   = gs.reset()
        self.assertEquals(state,[0,0,0,0,0,0,0,0,0])

    def test_valid_move(self):
        """ Tests valid move """
        gs      = GameState()
        state   = gs.reset()
        res     = gs.move(board.HUMAN_PLAYER,state,0)
        self.assertEquals(res[0],board.HUMAN_PLAYER)

    def test_invalid_move(self):
        """ Tests move to occupied space """
        gs      = GameState()
        state   = [1,0,0,0,0,0,0,0,0]
        res     = gs.move(board.HUMAN_PLAYER,state,0)
        self.assertEquals(res,None)

    def test_out_of_index_move(self):
        """ Tests for index out of range move """
        gs      = GameState()
        state   = gs.reset()
        res     = gs.move(board.HUMAN_PLAYER,state,15)
        self.assertEquals(res,None)

    def test_game_not_complete_empty(self):
        """ Tests for empty game complete """
        gs      = GameState()
        state   = gs.reset()
        self.assertEquals(gs.isGameOver(state),False)

    def test_game_not_complete_partial(self):
        """ Tests partially played game is not complete """
        gs      = GameState()
        state   = [1,0,0,1,-1,0,-1,1,0]
        self.assertEquals(gs.isGameOver(state),False)

    def test_game_no_winner(self):
        """ Tests game has no winner """
        gs      = GameState()
        state   = gs.reset()
        self.assertEquals(gs.getWinner(state),None)

        state   = [1,1,-1,0,0,0,0,0,0]
        self.assertEquals(gs.getWinner(state),None)

    def test_game_win_rows(self):
        """ Tests win by rows """
        gs      = GameState()
        state   = [1,1,1,0,0,0,0,0,0]
        self.assertEquals(gs.getWinner(state),1)

        state   = [0,0,0,1,1,1,0,0,0]
        self.assertEquals(gs.getWinner(state),1)

        state   = [0,0,0,0,0,0,1,1,1]
        self.assertEquals(gs.getWinner(state),1)

    def test_game_win_columns(self):
        """ Tests win by columns """
        gs      = GameState()
        state   = [1,0,0,1,0,0,1,0,0]
        self.assertEquals(gs.getWinner(state),1)

        state   = [0,1,0,0,1,0,0,1,0]
        self.assertEquals(gs.getWinner(state),1)

        state   = [0,0,1,0,0,1,0,0,1]
        self.assertEquals(gs.getWinner(state),1)

    def test_game_win_diagonals(self):
        """ Tests win by diagonals """
        gs      = GameState()
        state   = [1,0,0,0,1,0,0,0,1]
        self.assertEquals(gs.getWinner(state),1)

        state   = [0,0,1,0,1,0,1,0,0]
        self.assertEquals(gs.getWinner(state),1)

