class HumanPlayer:
    def __init__(self, mark):
        self.mark = mark
        self.game_state = None
        self.is_my_turn = False
        self.callback = None

    def play(self, game_state, callback, first_move=False):
        self.is_my_turn = True
        input_successful = False
        while not input_successful:
            action = input("Please enter your action (integer 0 - 8): ")
            try:
                action_id = int(action)
                input_successful = True
            except:
                print("Invalid input")
        callback(action_id, self.mark, self.reward_me)

    def reward_me(self, reward, new_game_state, game_over=False):
        if game_over:
            # TODO: notification popup
            pass
        # discard everything we receive, we just need this method so that
        # the interface between all the player types is identical