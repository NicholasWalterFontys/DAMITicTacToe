from keras.models import Sequential
from keras.layers.core import *
from keras.optimizers import RMSprop
import random
import numpy as np


class Player:
    def __init__(self, mark):
        self.mark = mark

        self.game_state = None
        self.action = None
        self.log = [] # prior game state, action, reward, later game state

        self.model = self.init_model()
        self.epsilon = 1
        self.step_counter = 0

    @staticmethod
    def init_model(self):
        model = Sequential()

        # one layer consists of a "calculation" part, the activation function
        # and a Dropout layer which prevents overfitting

        # units --> number of output values in this case x and y for
        # tic tac toe field
        # 3*3 because we have a field size of 3 by 3 segments

        # input_shape --> number of input values in this case one for each
        # segment of the tic tac toe field
        model.add(Dense(
            units=3*3, input_shape=9
        ))

        model.add(Activation('relu'))
        model.add(Dropout(0.2))

        model.add(Dense(
            units=3*3, input_shape=9
        ))

        model.add(Activation('relu'))
        model.add(Dropout(0.2))

        model.add(Dense(
            units=3*3, init='lecun_uniform'
        ))
        model.add(Activation('linear'))

        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)

        return model

    def play(self, game_state, callback, first_move=False):
        self.game_state = game_state # save old game state
        self.step_counter += 1
        if self.step_counter % 100 == 0 and self.epsilon > 0:
            self.epsilon -= 0.01

        if random.random() < self.epsilon:
            # select random field segment to play on
            self.action = random.randint(0, 8)
        else:
            qvals = self.model.predict(game_state, batch_size=1)
            print(qvals) # TODO: remove debug
            if first_move:
                qvals[4] = 0
            self.action = np.argmax(qvals)
            # calculate action
            # save action
            # send action to GameManager
        callback(self.action, self.mark, self.reward_me)

    def reward_me(self, reward, new_game_state):
        # receive reward
        # receive new game state
        # save replay as [State, Action, Reward, NewState]

        self.log.append([self.game_state, self.action, reward, new_game_state])
        pass