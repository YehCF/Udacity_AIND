"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import numpy as np

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    # step differences
    player_moves = game.get_legal_moves(player = player)
    opponent_moves = game.get_legal_moves(player = game.get_opponent(player))
    move_difference = len(player_moves) - len(opponent_moves)
    same_moves = len(set(player_moves) - set(opponent_moves))
    
    # location
    player_x, player_y = game.get_player_location(player = player)
    opponent_x, opponent_y = game.get_player_location(player = game.get_opponent(player))

    if move_difference > 0:
        return move_difference + (float(abs(player_x-opponent_x) + abs(player_y-opponent_y))) - same_moves
    else:
        return move_difference + -1*(float(abs(player_x-opponent_x) + abs(player_y-opponent_y))) - same_moves



'''
    # Get the difference of legal moves between player and its opponent
    player_moves = game.get_legal_moves(player = player)
    opponent_moves = game.get_legal_moves(player = game.get_opponent(player))
    move_difference = len(player_moves) - len(opponent_moves)

    # get player's and opponent's locations
    player_x, player_y = game.get_player_location(player = player)
    opponent_x, opponent_y = game.get_player_location(player = game.get_opponent(player))

    # center of the game
    center_x, center_y = game.width / 2., game.height/2.

    
    
    return -1*float(abs(abs(player_x-center_x) + abs(player_y-center_y) - 1.5)) + \
    -1*float(abs(player_x-opponent_x) + abs(player_y-opponent_y)) + (move_difference)
'''
    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    
    # step differences
    player_moves = game.get_legal_moves(player = player)
    opponent_moves = game.get_legal_moves(player = game.get_opponent(player))
    move_difference = len(player_moves) - len(opponent_moves)
    
    # location
    player_x, player_y = game.get_player_location(player = player)
    opponent_x, opponent_y = game.get_player_location(player = game.get_opponent(player))

    if move_difference > 0:
    	return (move_difference)*(float(abs(player_x-opponent_x) + abs(player_y-opponent_y)))
    else:
    	return abs(move_difference)*-1*(float(abs(player_x-opponent_x) + abs(player_y-opponent_y)))



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    # step differences
    player_moves = game.get_legal_moves(player = player)
    opponent_moves = game.get_legal_moves(player = game.get_opponent(player))
    move_difference = len(player_moves) - len(opponent_moves)
    same_moves = len(set(player_moves) - set(opponent_moves))

    # location
    player_x, player_y = game.get_player_location(player = player)
    opponent_x, opponent_y = game.get_player_location(player = game.get_opponent(player))

    if move_difference > 0:
        return (move_difference) + (float(abs(player_x-opponent_x) + abs(player_y-opponent_y))) + same_moves
    else:
        return (move_difference) + -1*(float(abs(player_x-opponent_x) + abs(player_y-opponent_y))) - same_moves

'''    
    # same steps
    player_moves = game.get_legal_moves(player = player)
    opponent_moves = game.get_legal_moves(player = game.get_opponent(player))

    same_steps = len(set(player_moves) - set(opponent_moves))

    # distance from opponent
    player_x, player_y = game.get_player_location(player = player)
    opponent_x, opponent_y = game.get_player_location(player = game.get_opponent(player))
    
    distance = abs(player_x - opponent_x) + abs(player_y - opponent_y)

    return float(same_steps + 1.0/distance)
'''



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        
        # Max Function: Get the Greatest move possibilities
        def max_value(game_state, current_depth):
            # timer check
            #print("Current:", current_depth, ";depth:", depth)
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Terminal-Test (if at terminal, return self's possible moves)
            if game_state.utility(self) != 0 : 
                return self.score(game_state, self)
                #return game_state.utility(self)
            # depth check (if equal, return self's possible moves from state at depth)
            if current_depth == depth:
                return self.score(game_state, self)

            # get max value of move possibilities
            value = float("-inf")
            for possible_move in game_state.get_legal_moves():
                possible_game_state = game_state.forecast_move(possible_move)
                value = max([value, min_value(possible_game_state, current_depth+1)])
            return value

        # Min Function: Get the Smallest move possibilities
        def min_value(game_state, current_depth):
            # timer check
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Terminal-Test (if at terminal, return self's possible moves)
            if game_state.utility(self) != 0: 
                return self.score(game_state, self)
                #return game_state.utility(self)
            # depth check (if equal, return self's possible moves from state at depth)
            if current_depth == depth:
                return self.score(game_state, self)
                
            # get min value of move possiblities
            value = float("inf")
            for possible_move in game_state.get_legal_moves():
                possible_game_state = game_state.forecast_move(possible_move)
                value = min([value, max_value(possible_game_state, current_depth+1)])
            return value

        # Main: Get the move that contains the most possibilities for the current state
        
        # get possible moves from the current state
        current_possible_moves = game.get_legal_moves()
        if len(current_possible_moves) == 0:
            return (-1, -1)
        # scores of all moves
        scores_of_possible_moves = []
        # set current depth 
        initial_depth = 0
        for current_possible_move in current_possible_moves:
            next_possible_game_state = game.forecast_move(current_possible_move)
            scores_of_possible_moves.append(min_value(next_possible_game_state, initial_depth + 1))
        return current_possible_moves[np.argmax(np.array(scores_of_possible_moves))]


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # best move
        best_move = (-1, -1)

        try:
        	depth = 0
        	while self.time_left() > self.TIMER_THRESHOLD:
        		depth += 1
        		best_move = self.alphabeta(game, depth)
        except SearchTimeout:
        	#print("Search depth:", depth, " Best move:", best_move)
        	pass
        return best_move

        # TODO: finish this function!
        #raise NotImplementedError
        #return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        #raise NotImplementedError

        # Max Function: Get the Greatest move possibilities after pruning
        def max_value(game_state, current_depth, alpha, beta):
            # Time check
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # depth check
            if current_depth == depth:
                return self.score(game_state, self)
            # Terminal test
            if game_state.utility(self) != 0:
                return self.score(game_state, self)
            # get max value of move possibilities
            value = float("-inf")
            # iterate through every possible moves
            for possible_move in game_state.get_legal_moves():
                possible_game_state = game_state.forecast_move(possible_move)
                value = max(value, min_value(possible_game_state, current_depth + 1, alpha, beta))
                # if value is greater than beta -> prune the rest of nodes
                if value >= beta: 
                    return value
                # update alpha
                alpha = max(alpha, value)
            return value

        # Min Function: Get the Smallest move possibilities after pruning
        def min_value(game_state, current_depth, alpha, beta):
            # Time check
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Depth check
            if current_depth == depth:
                return self.score(game_state, self)
            # Terminal Test
            if game_state.utility(self) != 0:
                return self.score(game_state, self)
            # get min value of move possibilities
            value = float("inf")
            # iterate through every possible moves
            for possible_move in game_state.get_legal_moves():
                possible_game_state = game_state.forecast_move(possible_move)
                value = min(value, max_value(possible_game_state, current_depth + 1, alpha, beta))
                # if value is lesser than alpha -> prune the rest of nodes
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value
        
        # Main: Choose a best_step after alpha-beta pruning
        # get the current possible moves
        current_possible_moves = game.get_legal_moves()
        if len(current_possible_moves) == 0:
        	return (-1,-1)
        initial_depth = 0
        scores_of_possible_moves = []
		# iterate through current possible moves        
        for current_possible_move in current_possible_moves:
            next_possible_game_state = game.forecast_move(current_possible_move)
            score = min_value(next_possible_game_state, initial_depth + 1, alpha, beta)
            # update alpha value
            alpha = max(alpha, score)
            scores_of_possible_moves.append(score)
        return current_possible_moves[np.argmax(np.array(scores_of_possible_moves))]


