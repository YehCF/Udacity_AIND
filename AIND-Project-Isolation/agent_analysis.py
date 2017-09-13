
from isolation import Board

import game_agent
import random
import timeit
from copy import copy
import sample_players

'''
	The file to implement heuristic analysis
'''
TIME_LIMIT_MILLIS = 150

class AnalysisBoard(Board):
	'''
		inherited Board
	'''
	def play(self, time_limit=TIME_LIMIT_MILLIS):
		"""Execute a match between the players by alternately soliciting them
		to select a move and applying it in the game.

		Parameters
		----------
		time_limit : numeric (optional)
		    The maximum number of milliseconds to allow before timeout
		    during each turn.

		Returns
		----------
		(player, list<[(int, int),]>, str)
		    Return multiple including the winning player, the complete game
		    move history, and a string indicating the reason for losing
		    (e.g., timeout or invalid move).
        """
		move_history = []

		time_millis = lambda: 1000 * timeit.default_timer()

		while True:

			legal_player_moves = self.get_legal_moves()
			game_copy = self.copy()

			move_start = time_millis()
			time_left = lambda : time_limit - (time_millis() - move_start)
			curr_move = self._active_player.get_move(game_copy, time_left)
			move_end = time_left()

			if curr_move is None:
			    curr_move = Board.NOT_MOVED

			if move_end < 0:
			    return self._inactive_player, move_history, "timeout"

			if curr_move not in legal_player_moves:
			    if len(legal_player_moves) > 0:
			        return self._inactive_player, move_history, "forfeit"
			    return self._inactive_player, move_history, "illegal move"

			move_history.append(list(curr_move))

			self.apply_move(curr_move)




if __name__ == '__main__':
	
	# create players

	player1 = game_agent.AlphaBetaPlayer(score_fn=game_agent.custom_score_3)
	player2 = game_agent.AlphaBetaPlayer(score_fn=game_agent.custom_score)

	# set up game board
	game = AnalysisBoard(player1, player2)

	# get moves
	for _ in range(2):
		move = random.choice(game.get_legal_moves())
		game.apply_move(move)

	print("----First Moves----")
	print(game.to_string())

	winner, history, outcome = game.play()
	if winner == player1:
		win = "player1"
	else:
		win = "player2"
	print("\nWinner: {}\n{}\nOutcome: {}".format(winner, win, outcome))
	print(game.to_string())
	print("Move history:\n{!s}".format(history))


