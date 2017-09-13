"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.AlphaBetaPlayer(score_fn = game_agent.custom_score)
        self.player2 = game_agent.AlphaBetaPlayer(score_fn = sample_players.improved_score)
        self.game = isolation.Board(self.player1, self.player2)

    def heuristicTest(self):

        # initialize moves
        for _ in range(2):
            move = random.choice(self.game.get_legal_moves())
            game.apply_move(move)

        # print out the first two moves
        print(self.game.to_string())
        print("Yes")




if __name__ == '__main__':
    print("A")
    unittest.main()





