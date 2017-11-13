class Player:
    def __init__(self):
        self.game_state = None
        self.action = None
        pass

    def play(self, game_state, callback, first_move=False):
        # receive game state
        # save game state
        # calculate action
        # save action
        # send action to GameManager
        pass

    def reward_me(self, reward, new_game_state):
        # receive reward
        # receive new game state
        # save replay as [State, Action, Reward, NewState]
        pass