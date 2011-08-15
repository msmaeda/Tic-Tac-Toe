HUMAN_PLAYER    =   1
COMPUTER_PLAYER =   -1

WINS            =   [[0,1,2],[3,4,5],[6,7,8],
                     [0,3,6],[1,4,7],[2,5,8],
                     [0,4,8],[2,4,6]]

class GameState(object):
    """ Manages game state """

    def reset(self):
        return  [0,0,0,0,0,0,0,0,0]

    def move(self,player,state,position):
        """ Returns new state if valid move, None if not """
        try:
            if state[position] != 0:
                return None
            else:
                state[position]    = player
                return state
        except IndexError:
            return None

    def isGameOver(self,state):
        """ Returns true if complete, false if not """
        return (self.getWinner(state) is not None or 0 not in state)

    def getWinner(self,state):
        """ Returns winner or None if no winner """
        for win in WINS:
            if state[win[0]] == state[win[1]] == state[win[2]] and state[win[0]] != 0:
                return state[win[0]]

        return None
