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

        self.statistic.started_game(self.current_player.mark)

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
        rewards = np.zeros(9)

        for i in range(9):
            # get coordinates and translated game state (from 1D to 2D array)
            x, y, tgs = self.translate_coordinate(i)

            if self.game_state[i] != 0:
                rewards[i] = INVALID_REWARD
                continue

            # apply our action
            tgs[x][y] = mark

            # intial reward is zero
            reward = 0


            game_end_status = 0

            # check if current player won the game
            if self.check_win(x, y, tgs, mark):
                reward += WIN_REWARD
                # only save game status if this is the actual action the player
                # carried out
                if i == action:
                    print(self.translate_coordinate(1)[2])
                    print("win player " + str(mark))
                    game_end_status = 1
                    self.statistic.win(mark)

            # check if current action resulted in a draw
            elif self.check_draw(x, y, tgs, mark):
                reward += DRAW_REWARD
                # only save game status if this is the actual action the player
                # carried out
                if i == action:
                    print(self.translate_coordinate(1)[2])
                    print("draw")
                    game_end_status = 2
                    self.statistic.draw()

            # check if our current action gives us a block of length 2
            two_count = self.check_two_neighbours(x, y, tgs, mark)
            reward += two_count * TWO_REWARD

            # calculate enemy mark
            if mark == 1:
                enemy_mark = 2
            else:
                enemy_mark = 1

            # check if our current action blocks an enemy move
            two_blocked_count = self.check_two_neighbours(x, y, tgs, enemy_mark)
            reward += two_blocked_count * TWO_BLOCK_REWARD

            # check if our current action blocks an enemy win
            win_blocked_count = self.check_win_blocked(x, y, tgs, mark, enemy_mark)
            reward += win_blocked_count * BLOCK_WIN_REWARD

            if two_count == 0 and two_blocked_count == 0 \
                    and win_blocked_count == 0 and game_end_status == 0:
                reward += ONE_REWARD

            # only save game state if this is the true action
            if i == action:
                self.game_state = tgs.reshape(9)

            rewards[i] = reward
        return rewards, game_end_status

    def check_win(self, x, y, tgs, mark):
        # sum of array equals 3 times mark --> array is full of mark
        if np.sum(tgs[y]) == mark * 3:
            return True
        # sum of column equals 3 times mark --> column is full of mark
        elif np.sum(tgs, axis=0)[y] == (mark*3):
            return True
        # check middle for mark, if set check opposing corners
        if tgs[1][1] == mark:
            if tgs[0][0] == mark and tgs[2][2] == mark:
                return True
            elif tgs[0][2] == mark  and tgs[2][0] == mark:
                return True
        return False

    def check_draw(self, x, y, tgs, mark):
        # check if all field segments are set
        for i in range(3):
            for j in range(3):
                if tgs[i][j] == 0:
                    return False
        return True

    def check_two_neighbours(self, x, y, tgs, mark):
        neighbours = self.get_neighbours(x, y)
        counter = 0
        for n in neighbours:
            if tgs[n[0], n[1]] == mark:
                counter += 1
        return counter

    def check_win_blocked(self, x, y, tgs, mark, enemy_mark):
        counter = 0
        blocked_value = (2* enemy_mark + mark)

        # handle rows and columns
        for i in range(2):
            nonzeroes = np.count_nonzero(tgs, axis=i)
            for j in nonzeroes:
                if j == 3:
                    sum = np.sum(tgs, axis=i)
                    for k in sum:
                        if k == blocked_value:
                            counter += 1

        # handle diagonals
        diag_a = [tgs[0, 0], tgs[1, 1], tgs[2, 2]]
        diag_b = [tgs[0, 2], tgs[1, 1], tgs[2, 0]]
        if np.count_nonzero(diag_a) == 3 and np.sum(diag_a) == blocked_value:
            counter += 1
        if np.count_nonzero(diag_b) == 3 and np.sum(diag_b) == blocked_value:
            counter += 1
        return counter

    def get_neighbours(self, x, y):
        id = x + 3* y

        neighbours = {
            0: [[0, 1], [1, 0], [1, 1]],
            1: [[0, 0], [0, 2], [1, 1]],
            2: [[0, 1], [1, 1], [1, 2]],
            3: [[0, 0], [1, 1], [1, 0]],
            4: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1],
                     [2, 2]],
            5: [[0, 2], [1, 1], [2, 2]],
            6: [[1, 0], [1, 1], [2, 1]],
            7: [[2, 0], [1, 1], [2, 2]],
            8: [[2, 1], [1, 1], [1, 2]]
        }

        return neighbours[id]
        """
        # doesnt work properly
        result = []
        for i in range(3):
            for j in range(3):
                dist_x = math.fabs(x - i)
                dist_y = math.fabs(y - j)
                dist_t = math.sqrt(dist_x + dist_y)
                if dist_t > 0 and dist_t < 2 and dist_x < 2 and dist_y < 2:
                    result.append([i, j])
        return result
        """

    def translate_coordinate(self, action):
        y = action
        x = 0
        while y >= 3:
            y -= 3
            x += 1
        temp_game_state = self.game_state.reshape((3, 3))
        return x, y , np.array(temp_game_state, copy=True)