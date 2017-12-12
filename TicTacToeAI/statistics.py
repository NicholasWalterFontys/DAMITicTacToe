import datetime
import json

class Statistic:
    def __init__(self, epsilon, total_games=0):
        self.epsilon = epsilon
        self.total_games = total_games

        self.game_log = []

        self.invalid_move_counter = {}
        self.game_starter = None
        self.game_started_time = None

        self.start_time = None
        self.end_time = None

        self.player_1_invalid_moves = 0
        self.player_4_invalid_moves = 0

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def game_started(self, starter):
        self.game_starter = starter
        self.game_started_time = datetime.datetime.now()

    def game_ended(self, end_game_state, winner=0):
        game_time = (datetime.datetime.now() - self.game_started_time).total_seconds()
        log = {"winner": winner,
               "starter": self.game_starter,
               "end_state": end_game_state,
               "inv_moves_1": self.player_1_invalid_moves,
               "inv_moves_4": self.player_4_invalid_moves,
               "epsilon": self.epsilon,
               "game_time": game_time}
        self.game_log.append(log)

        self.player_1_invalid_moves = 0
        self.player_4_invalid_moves = 0

        percentage_done = int((len(self.game_log) / self.total_games) * 100)
        t = "|" + "X" * percentage_done + "_" * (100 - percentage_done) + "|"
        print(t)

    def invalid_move(self, player):
        if player == 1:
            self.player_1_invalid_moves += 1
        else:
            self.player_4_invalid_moves += 1

    def started(self):
        self.start_time = datetime.datetime.now()

    def ended(self):
        self.end_time = datetime.datetime.now()

    def print_statistic(self):
        a = json.dumps(self.game_log, indent=4)
        with open("log.txt", "w") as target:
            target.write(a)
        print("TODO: print statistic")