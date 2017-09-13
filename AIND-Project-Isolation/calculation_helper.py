import numpy as np

x = list(range(0,7))
y = list(range(0,7))

moves = set([(i,j) for i in x for j in y])

past_steps = set([(4, 4), (2, 4), (3, 2), (0, 3), (5, 3), (2, 2), (3, 4), (3, 0), (4, 2), (5, 1), (5, 4)])

empty = moves - past_steps

next_move = set([(6,3)])

legal_move = set([(5,5)])

center = np.array(list(empty-next_move-legal_move)).mean(axis = 0)

distance = abs(center - np.array(list(next_move))).sum()

print(center)
print(distance)

#import numpy as np

#from game_agent import MinimaxPlayer, AlphaBetaPlayer




'''

if __name__ == "__main__":
    from isolation import Board

    # create an isolation board (by default 7x7)
    player1 = AlphaBetaPlayer()
    player2 = MinimaxPlayer()
    game = Board(player1, player2)

    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that the .apply_move() method changes the calling object in-place.
    game.apply_move((2, 4))
    game.apply_move((4, 4))
    print(game.to_string())

    # get empty moves (exclude player's legal moves)
    next_game_state = game.forecast_move((4,5))
    active_player = game.active_player
    print("active_player:", active_player)
    print("legal moves", next_game_state.get_legal_moves(player= active_player))
    empty_spaces = np.array(list(set(next_game_state.get_blank_spaces()) - set(next_game_state.get_legal_moves(player= active_player))))

    empty_space_center = empty_spaces.mean(axis = 0)
    print("Center:",empty_space_center)
    # get player's location
    player_x, player_y = next_game_state.get_player_location(player = active_player)

    distance =  -1*float(abs(empty_space_center[0]-player_x) + abs(empty_space_center[1]-player_y))
    
    print("Distance:", distance)
'''

'''
    # players take turns moving on the board, so player1 should be next to move
    assert(player1 == game.active_player)

    # get a list of the legal moves available to the active player
    print(game.get_legal_moves())

    # get a successor of the current state by making a copy of the board and
    # applying a move. Notice that this does NOT change the calling object
    # (unlike .apply_move()).
    new_game = game.forecast_move((1, 1))
    assert(new_game.to_string() != game.to_string())
    print("\nOld state:\n{}".format(game.to_string()))
    print("\nNew state:\n{}".format(new_game.to_string()))

    # play the remainder of the game automatically -- outcome can be "illegal
    # move", "timeout", or "forfeit"
    winner, history, outcome = game.play()
    print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    print(game.to_string())
    print("Move history:\n{!s}".format(history))
'''
