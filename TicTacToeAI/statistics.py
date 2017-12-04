import datetime

class Statistic:
    def __init__(self):
        self.win_counter_1 = 0
        self.win_counter_4 = 0
        self.start_counter_1 = 0
        self.start_counter_4 = 0
        self.draw_counter = 0
        self.start_time = None
        self.end_time = None

    def started(self):
        self.start_time = datetime.datetime.now()

    def ended(self):
        self.end_time = datetime.datetime.now()

    def draw(self):
        self.draw_counter += 1

    def win(self, mark):
        if mark == 1:
            self.win_counter_1 += 1
        else:
            self.win_counter_4 += 1

    def started_game(self, mark):
        if mark == 1:
            self.start_counter_1 += 1
        else:
            self.start_counter_4 += 1

    def print_statistic(self):
        print("total games: " + str(self.win_counter_1 + self.win_counter_4 + self.draw_counter))
        print("1 wins: " + str(self.win_counter_1))
        print("1 starts: " + str(self.start_counter_1))
        print("4 wins: " + str(self.win_counter_4))
        print("4 starts: " + str(self.start_counter_4))
        print("draws: " + str(self.draw_counter))
        print("-----\n\ntime taken: {}".format(self.end_time - self.start_time))