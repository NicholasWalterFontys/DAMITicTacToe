"""
The central game hub

Keeps the up-to-date game state, gives it to the two AI components and takes
their input each round
"""


class GameManager:
    def __init__(self, player_a, player_b):
        self.player_a = player_a
        self.player_b = player_b

        self.game_state = [[None, None, None]] * 3
        # decide which player begins

        self.current_player = None # TODO
        self.other_player = None

        # do one game iteration with first_move = True

    def game_loop(self):
        # pass game state to current player
        # do game iteration
        pass

    def action_callback(self, action):
        # receive action
        # evaluate action
        # give reward
        # return to game loop
        pass
