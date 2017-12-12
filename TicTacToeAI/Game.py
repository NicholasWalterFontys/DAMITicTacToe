"""
The central game hub

Keeps the up-to-date game state, gives it to the two AI components and takes
their input each round
"""
import numpy as np
import random
import math

WIN_REWARD = 500        # won the game
BLOCK_WIN_REWARD = 400  # blocked enemy win
TWO_REWARD = 300        # two in a line
TWO_BLOCK_REWARD = 200  # put one next to an enemy
ONE_REWARD = 100        # put one somewhere without any neighbours
DRAW_REWARD = 0         # game ended in a draw
LOST_REWARD = -500      # lost the game
INVALID_REWARD = -2000  # put invalid move


class GameManager:
    def __init__(self, player_a, player_b, stat, size=3):
        # select player to start
        self.game_over = False
        r = random.randint(0, 1)
        if r == 0:
            self.current_player = player_a
            self.other_player = player_b
        else:
            self.current_player = player_b
            self.other_player = player_a

        self.statistic = stat

        self.statistic.game_started(self.current_player.mark)

        # initialise game state
        self.game_state = np.zeros(9, dtype=np.int)

        # do one game iteration with first_move = True
        self.current_player.play(np.array(self.game_state, copy=True), self.action_callback, True)

        self.game_loop()

    def game_loop(self):
        while not self.game_over:
            # switch players
            temp = self.current_player
            self.current_player = self.other_player
            self.other_player = temp

            # game continues
            self.current_player.play(np.array(self.game_state, copy=True), self.action_callback)

    def action_callback(self, action, mark, reward_callback):
        # rewards --> total sum of rewards for this action to be given to the
        # current player
        # game_end_status --> 0 for nothing, 1 for won, 2 for draw --> give
        # feedback to enemy player
        rewards, game_end_status = self.apply_action(action, mark)

        # check if game is over, if so give rewards to other player
        if game_end_status == 1:
            self.other_player.reward_me(rewards,
                                        np.array(self.game_state, copy=True),
                                        True)
            reward_callback(rewards, np.array(self.game_state, copy=True), True)
            self.game_over = True
        elif game_end_status == 2:
            self.other_player.reward_me(rewards,
                                        np.array(self.game_state, copy=True),
                                        True)
            reward_callback(rewards, np.array(self.game_state, copy=True), True)
            self.game_over = True
        else:
            reward_callback(rewards, np.array(self.game_state, copy=True))

    def apply_action(self, action, mark):
        # target list for rewards of each field
        game_end_status = 0
        rewards = np.zeros(9)

        for i in range(9):
            # check if the currently evaluated move is invalid
            if self.game_state[i] != 0:
                rewards[i] = INVALID_REWARD
                if i == action:
                    self.statistic.invalid_move(mark)
                continue

            # apply our action
            tgs = np.array(self.game_state, copy=True)
            tgs[i] = mark

            # initial reward is zero
            reward = 0

            # check if current player won the game
            if self.check_win(tgs, mark):
                reward += WIN_REWARD
                # only save game status if this is the actual action the player
                # carried out
                if i == action:
                    game_end_status = 1
                    self.statistic.game_ended(np.array(tgs).reshape((3, 3)).tolist(), mark)
                    self.game_state = tgs

            # check if current action resulted in a draw
            elif self.check_draw(tgs):
                reward += DRAW_REWARD
                # only save game status if this is the actual action the player
                # carried out
                if i == action:
                    game_end_status = 2
                    self.statistic.game_ended(np.array(tgs).reshape((3, 3)).tolist())
                    self.game_state = tgs

            # check if our current action gives us a block of length 2
            two_count = self.check_two_neighbours(tgs, i, mark)
            reward += two_count * TWO_REWARD

            # calculate enemy mark
            if mark == 1:
                enemy_mark = 4
            else:
                enemy_mark = 1

            # check if our current action blocks an enemy move
            two_blocked_count = self.check_two_neighbours(tgs, i, enemy_mark)
            reward += two_blocked_count * TWO_BLOCK_REWARD

            # check if our current action blocks an enemy win
            win_blocked_count = self.check_win_blocked(tgs, mark, enemy_mark)
            reward += win_blocked_count * BLOCK_WIN_REWARD

            if two_count == 0 and two_blocked_count == 0 \
                    and win_blocked_count == 0 and game_end_status == 0:
                reward += ONE_REWARD

            # only save game state if this is the true action
            if i == action:
                self.game_state = tgs.reshape(9)

            rewards[i] = reward
        return rewards, game_end_status

    def check_win(self, tgs, mark):
        possible_wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                         [0, 3, 6], [1, 4, 7], [2, 5, 8],
                         [0, 4, 8], [2, 4, 6]]

        for pw in possible_wins:
            sum = 0
            for a in pw:
                sum += tgs[a]
            if sum == mark * 3:
                return True
        return False

    def check_draw(self, tgs):
        for a in tgs:
            if a == 0:
                return False
        return True

    def check_two_neighbours(self, tgs, i, mark):
        neighbours = self.get_neighbours(i)
        counter = 0
        for n in neighbours:
            if tgs[n] == mark:
                counter += 1
        return counter

    def check_win_blocked(self, tgs, mark, enemy_mark):
        counter = 0
        blocked_value = (2* enemy_mark + mark)

        possible_wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                         [0, 3, 6], [1, 4, 7], [2, 5, 8],
                         [0, 4, 8], [2, 4, 6]]

        for pw in possible_wins:
            sum = 0
            for a in pw:
                sum += tgs[a]
            if sum == blocked_value:
                counter += 1
        return counter

    def get_neighbours(self, i):
        # not only direct neighbours but also opposing
        # e.g. 0/0 and 2/2 because they should count for two in a row
        # and two blocked
        neighbours = [[1, 3, 4, 8],
                      [0, 4, 2, 7],
                      [1, 4, 5, 6],
                      [0, 4, 6, 5],
                      [0, 1, 2, 3, 5, 6, 7, 8],
                      [2, 4, 8, 3],
                      [3, 4, 7, 2],
                      [6, 4, 8, 1],
                      [7, 4, 5, 0]]
        return neighbours[i]

    def translate_coordinate(self, action):
        y = action
        x = 0
        while y >= 3:
            y -= 3
            x += 1
        temp_game_state = self.game_state.reshape((3, 3))
        return x, y, np.array(temp_game_state, copy=True)