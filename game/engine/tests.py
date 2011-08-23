from django.test import TestCase
from django.test import Client
from django.utils import simplejson
from engine import board
from engine.board import GameState
from engine.bot import botMove

H   = board.HUMAN_PLAYER
C   = board.COMPUTER_PLAYER

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
        res     = gs.move(H,state,0)
        self.assertEquals(res[0],H)

    def test_invalid_move(self):
        """ Tests move to occupied space """
        gs      = GameState()
        state   = [1,0,0,0,0,0,0,0,0]
        res     = gs.move(H,state,0)
        self.assertEquals(res,None)

    def test_out_of_index_move(self):
        """ Tests for index out of range move """
        gs      = GameState()
        state   = gs.reset()
        res     = gs.move(H,state,15)
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

class TestBotMove(TestCase):
    """ Unit tests for bot move """

    def test_go_for_win_row(self):
        """ Tests that bot goes for win in row"""
        state   = [0,C,C,0,0,0,0,0,0]
        self.assertEquals(botMove(state),0)

        state   = [C,0,C,0,0,0,0,0,0]
        self.assertEquals(botMove(state),1)

        state   = [C,C,0,0,0,0,0,0,0]
        self.assertEquals(botMove(state),2)

        state   = [0,0,0,0,C,C,0,0,0]
        self.assertEquals(botMove(state),3)

        state   = [0,0,0,C,0,C,0,0,0]
        self.assertEquals(botMove(state),4)

        state   = [0,0,0,C,C,0,0,0,0]
        self.assertEquals(botMove(state),5)

        state   = [0,0,0,0,0,0,0,C,C]
        self.assertEquals(botMove(state),6)

        state   = [0,0,0,0,0,0,C,0,C]
        self.assertEquals(botMove(state),7)

        state   = [0,0,0,0,0,0,C,C,0]
        self.assertEquals(botMove(state),8)


    def test_go_for_win_column(self):
        """ Tests that bot goes for win in column"""
        state   = [0,0,0,C,0,0,C,0,0]
        self.assertEquals(botMove(state),0)

        state   = [C,0,0,0,0,0,C,0,0]
        self.assertEquals(botMove(state),3)

        state   = [C,0,0,C,0,0,0,0,0]
        self.assertEquals(botMove(state),6)

        state   = [0,0,0,0,C,0,0,C,0]
        self.assertEquals(botMove(state),1)

        state   = [0,C,0,0,0,0,0,C,0]
        self.assertEquals(botMove(state),4)

        state   = [0,C,0,0,C,0,0,0,0]
        self.assertEquals(botMove(state),7)

        state   = [0,0,0,0,0,C,0,0,C]
        self.assertEquals(botMove(state),2)

        state   = [0,0,C,0,0,0,0,0,C]
        self.assertEquals(botMove(state),5)

        state   = [0,0,C,0,0,C,0,0,0]
        self.assertEquals(botMove(state),8)

    def test_go_win_diagonal(self):
        """ Tests that bot goes for win in diagonals """
        state   = [0,0,0,0,C,0,0,0,C]
        self.assertEquals(botMove(state),0)

        state   = [C,0,0,0,0,0,0,0,C]
        self.assertEquals(botMove(state),4)

        state   = [C,0,0,0,C,0,0,0,0]
        self.assertEquals(botMove(state),8)

        state   = [0,0,0,0,C,0,C,0,0]
        self.assertEquals(botMove(state),2)

        state   = [0,0,C,0,0,0,C,0,0]
        self.assertEquals(botMove(state),4)

        state   = [0,0,C,0,C,0,0,0,0]
        self.assertEquals(botMove(state),6)

    def test_block_win_row(self):
        """ Tests that bot blocks player win in rows"""
        state   = [0,H,H,0,0,0,0,0,0]
        self.assertEquals(botMove(state),0)

        state   = [H,0,H,0,0,0,0,0,0]
        self.assertEquals(botMove(state),1)

        state   = [H,H,0,0,0,0,0,0,0]
        self.assertEquals(botMove(state),2)

        state   = [0,0,0,0,H,H,0,0,0]
        self.assertEquals(botMove(state),3)

        state   = [0,0,0,H,0,H,0,0,0]
        self.assertEquals(botMove(state),4)

        state   = [0,0,0,H,H,0,0,0,0]
        self.assertEquals(botMove(state),5)

        state   = [0,0,0,0,0,0,0,H,H]
        self.assertEquals(botMove(state),6)

        state   = [0,0,0,0,0,0,H,0,H]
        self.assertEquals(botMove(state),7)

        state   = [0,0,0,0,0,0,H,H,0]
        self.assertEquals(botMove(state),8)

    def test_block_win_column(self):
        """ Tests that bot blocks player win in columns """
        state   = [0,0,0,H,0,0,H,0,0]
        self.assertEquals(botMove(state),0)

        state   = [H,0,0,0,0,0,H,0,0]
        self.assertEquals(botMove(state),3)

        state   = [H,0,0,H,0,0,0,0,0]
        self.assertEquals(botMove(state),6)

        state   = [0,0,0,0,H,0,0,H,0]
        self.assertEquals(botMove(state),1)

        state   = [0,H,0,0,0,0,0,H,0]
        self.assertEquals(botMove(state),4)

        state   = [0,H,0,0,H,0,0,0,0]
        self.assertEquals(botMove(state),7)

        state   = [0,0,0,0,0,H,0,0,H]
        self.assertEquals(botMove(state),2)

        state   = [0,0,H,0,0,0,0,0,H]
        self.assertEquals(botMove(state),5)

        state   = [0,0,H,0,0,H,0,0,0]
        self.assertEquals(botMove(state),8)

    def test_block_win_diagonal(self):
        """ Tests that bot blocks player win in diagonals """

        state   = [0,0,0,0,H,0,0,0,H]
        self.assertEquals(botMove(state),0)

        state   = [H,0,0,0,0,0,0,0,H]
        self.assertEquals(botMove(state),4)

        state   = [H,0,0,0,H,0,0,0,0]
        self.assertEquals(botMove(state),8)

        state   = [0,0,0,0,H,0,H,0,0]
        self.assertEquals(botMove(state),2)

        state   = [0,0,H,0,0,0,H,0,0]
        self.assertEquals(botMove(state),4)

        state   = [0,0,H,0,H,0,0,0,0]
        self.assertEquals(botMove(state),6)

    def test_best_move_takes_center(self):
        """ Tests that bot takes center if avaiable """
        state   = [H,0,0,0,0,0,0,0,0]
        self.assertEquals(botMove(state),4)

    def test_best_move_takes_corner(self):
        """ Tests that bot takes first corner if center not available """
        state   = [0,0,0,0,H,0,0,0,0]
        self.assertEquals(botMove(state),0)

    def test_best_move_has_center_selects_open_side(self):
        """ Tests that bot takes first or second side if available """
        state   = [H,0,0,0,C,H,0,0,0]
        self.assertEquals(botMove(state),1)

        state   = [H,0,0,0,C,0,0,H,0]
        self.assertEquals(botMove(state),3)

    def test_best_move_has_corner_avoids_fork(self):
        """ Tests that bot takes corner to avoid fork """
        state   = [C,0,0,0,H,0,0,0,H]
        self.assertEquals(botMove(state),2)

    def test_best_move_has_center_avoids_fork(self):
        """ Tests that bot takes appropriate corner to avoid fork """
        state   = [0,H,0,H,C,0,0,0,0]
        self.assertEquals(botMove(state),0)

        state   = [0,H,0,0,C,H,0,0,0]
        self.assertEquals(botMove(state),0)

        state   = [0,0,0,H,C,0,0,H,0]
        self.assertEquals(botMove(state),8)

        state   = [0,0,0,0,C,H,0,H,0]
        self.assertEquals(botMove(state),8)

    def test_best_move_has_fork_opportunity(self):
        """ Tests that bot takes fork opportunity if available """
        state   = [0,H,0,C,C,H,0,H,0]
        self.assertEquals(botMove(state),0)

        state   = [0,C,0,H,C,H,0,H,0]
        self.assertEquals(botMove(state),0)

    def test_best_move_closing_play(self):
        """ Tests that bot makes last optimum play if at this state """
        state   = [H,C,0,0,C,H,0,H,0]
        self.assertEquals(botMove(state),8)

        state   = [C,H,0,H,C,0,0,0,H]
        self.assertEquals(botMove(state),2)

class WebTest(TestCase):
    """ Unit tests for web interface """

    def test_main_page(self):
        """ Tests main page is presented on open """
        c           = Client()
        response    = c.get('/')
        self.assertEquals(response.status_code,200)
        self.assertContains(response, 'Your Move First')

    def test_player_move_game_over_tie(self):
        """ Tests json returned when tie game """
        c           = Client()
        response    = c.get('/move/8/121122210')
        self.assertEquals(response.status_code,200)
        self.assertEqual(simplejson.loads(str(response.content))['status'],'gameover')
        self.assertEqual(simplejson.loads(str(response.content))['msg'],'Tie Game')

    def test_player_move_game_over_player_win(self):
        """ Tests json returned when player wins """
        c           = Client()
        response    = c.get('/move/2/110220102')
        self.assertEquals(response.status_code,200)
        self.assertEqual(simplejson.loads(str(response.content))['status'],'gameover')
        self.assertEqual(simplejson.loads(str(response.content))['msg'],'Player Wins!')

    def test_player_move_game_over_computer_win(self):
        """ Test json returned when computer wins """
        c           = Client()
        response    = c.get('/move/6/210221010')
        self.assertEquals(response.status_code,200)
        self.assertEqual(simplejson.loads(str(response.content))['status'],'gameover')
        self.assertEqual(simplejson.loads(str(response.content))['msg'],'Computer Wins!')

    def test_player_move_out_of_range(self):
        """ Test json returned when out of index range selected """
        c           = Client()
        response    = c.get('/move/10/000000000')
        self.assertEquals(response.status_code,200)
        self.assertEqual(simplejson.loads(str(response.content))['status'],'err')
        self.assertEqual(simplejson.loads(str(response.content))['msg'],'Invalid move')

        response    = c.get('/move/0/100000000')
        self.assertEquals(response.status_code,200)
        self.assertEqual(simplejson.loads(str(response.content))['status'],'err')
        self.assertEqual(simplejson.loads(str(response.content))['msg'],'Invalid move')

    def test_player_move_next_move(self):
        """ Tests json returned when player makes move and is now the next turn """
        c           = Client()
        response    = c.get('/move/0/000000000')
        self.assertEquals(response.status_code,200)
        self.assertEqual(simplejson.loads(str(response.content))['status'],'ok')
        self.assertEqual(simplejson.loads(str(response.content))['msg'],'Your move')

