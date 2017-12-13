from keras.models import Sequential
from keras.layers.core import *
from keras.optimizers import RMSprop
import random
import numpy as np

EPSILON_INTERVAL = 100
SAVE_INTERVAL = 25000


class Player:
    def __init__(self, mark, epsilon, model, print_status=False):
        self.mark = mark

        self.game_state = None
        self.action = None
        self.log = []  # prior game state, action, later game state, reward

        self.model = model
        self.epsilon = epsilon
        self.step_counter = 0

        self.print_status = print_status

    def play(self, game_state, callback):
        self.game_state = game_state  # save old game state
        self.step_counter += 1
        if random.random() < self.epsilon:
            # select random field segment to play on
            self.action = random.randint(0, 8)
        else:
            # target to predict from is the current game state
            target = game_state.tolist()

            qvals = self.model.model.predict(np.array([target]), batch_size=1)

            # get the action with the highest value
            self.action = np.argmax(qvals)
        if self.print_status:
            print("Ai player action: " + str(self.action))
        callback(self.action, self.mark, self.reward_me)

    def reward_me(self, rewards, new_game_state, game_over=False):
        X = np.array([new_game_state])
        Y = np.array([rewards.tolist()])
        self.model.model.fit(X, Y, verbose=False)