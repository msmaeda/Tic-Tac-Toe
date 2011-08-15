from engine import board

def botMove(state):
    """ Returns position for optimum move for bot, None if no move is possible """
    turn    = 10 - len(filter(lambda n: n == 0, state))

    if turn > 9:
        return None

    # Go for win
    for win in board.WINS:
        if (state[win[0]] + state[win[1]] + state[win[2]]) == (board.COMPUTER_PLAYER * 2):
            idx = [state[win[0]],state[win[1]],state[win[2]]].index(0)
            return win[idx]

    # Block win
    for win in board.WINS:
        if (state[win[0]] + state[win[1]] + state[win[2]]) == (board.HUMAN_PLAYER * 2):
            idx = [state[win[0]],state[win[1]],state[win[2]]].index(0)
            return win[idx]

    # Best move
    if turn == 2:
        # take center if available
        if state[4] == 0:
            return 4
        # take first corner if center is not available
        else:
            return 0
    elif turn == 4:
        # if computer owns center
        if state[4] == board.COMPUTER_PLAYER:
            # If center row or column has two open spaces, select side
            if state[1] == state[7] == 0:
                return 1
            elif state[3] == state[5] == 0:
                return 3
            # player may try to fork from corner
            else:
                if state[1] == board.HUMAN_PLAYER:
                    return 0
                else:
                    return 8
        # if computer owns first corner
        else:
            # If bot has corner and we are not blocking by this point
            # it means human has both the center and opposite corner
            # of board and is potentially setting up a fork, select 
            # open corner
            return 2
    elif turn == 6:
        # By this point, either block last remaining fork opportunity,
        # fork to win or set up for tie game or win
        # Computer player should have the center in this case
        if state[0] == state[2] == state[6] == state[8] == 0:
            return 0
        else:
            # take last corner if open
            if state[8] == 0:
                return 8
            else:
                # If here, then computer owns center and the second side
                # Second corner should be chosen to avoid the fork
                if state[2] == 0:
                    return 2
                else:
                    raise Exception("Somthing is very wrong")
                    
