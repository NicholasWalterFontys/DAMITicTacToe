import datetime
import json

class Statistic:
    def __init__(self, total_games=0):
        self.total_games = total_games

        self.game_log = []

        self.invalid_move_counter = {}
        self.game_starter = None
        self.game_started_time = None

        self.start_time = None
        self.end_time = None

    def game_started(self, starter):
        self.game_starter = starter
        self.game_started_time = datetime.datetime.now()

    def game_ended(self, end_game_state, winner=0):
        game_time = (datetime.datetime.now() - self.game_started_time).total_seconds()
        log = {"winner": winner,
               "starter": self.game_starter,
               "end_state": end_game_state,
               "inv_moves": self.invalid_move_counter,
               "game_time": game_time}
        self.game_log.append(log)

        self.invalid_move_counter = {}

        percentage_done = int((len(self.game_log) / self.total_games) * 100)
        t = "|" + "X" * percentage_done + "_" * (100 - percentage_done) + "|"
        #print("{} per cent done".format(percentage_done))
        print(t)

    def invalid_move(self, player):
        if player not in self.invalid_move_counter:
            self.invalid_move_counter[player] = 0
        self.invalid_move_counter[player] += 1

    def started(self):
        self.start_time = datetime.datetime.now()

    def ended(self):
        self.end_time = datetime.datetime.now()

    def print_statistic(self):
        a = json.dumps(self.game_log, indent=4)
        with open("log.txt", "w") as target:
            target.write(a)
        print("TODO: print statistic")