import datetime
from keras.models import Sequential
from keras.layers.core import *
from keras.optimizers import RMSprop
import random
import numpy as np

EPSILON_INTERVAL = 100
SAVE_INTERVAL = 25000


def init_model():
    model = Sequential()

    # one layer consists of a "calculation" part, the activation function
    # and a Dropout layer which prevents overfitting

    # units --> number of output values in this case x and y for
    # tic tac toe field
    # 3*3 because we have a field size of 3 by 3 segments

    # input_shape --> number of input values in this case one for each
    # segment of the tic tac toe field

    """
    model.add(Dense(1, batch_input_shape=(4,3)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    """

    # input dim --> 9 for prior gs, 9 for later gs, 1 for action
    #model.add(Dense(9, input_shape=(9,), kernel_initializer='normal',
    #                activation='relu'))
    model.add(Dense(9, input_dim=9, kernel_initializer='normal',
                    activation='relu'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


class Player:
    def __init__(self, mark, epsilon, new_start=False):
        self.mark = mark

        self.game_state = None
        self.action = None
        self.log = [] # prior game state, action, later game state, reward

        self.model = init_model()
        self.epsilon = epsilon
        self.step_counter = 0

        # load model if this is not the first time we are running this
        if new_start:
            self.model.load_weights("saved-models/log_{}.h5".format(self.mark))

    def play(self, game_state, callback, first_move=False):
        self.game_state = game_state # save old game state
        self.step_counter += 1
        if random.random() < self.epsilon:
            # select random field segment to play on
            self.action = random.randint(0, 8)
        else:
            # target to predict from is the current game state
            target = game_state.tolist()

            qvals = self.model.predict(np.array([target]), batch_size=1)

            # get the action with the highest value
            self.action = np.argmax(qvals)
            print("learned action player {}: ".format(self.mark) + str(self.action))
        callback(self.action, self.mark, self.reward_me)

    def reward_me(self, rewards, new_game_state, game_over=False):
        # receive reward
        # receive new game state
        # save replay as [State, Action, NewState, Reward]

        X = np.array([new_game_state])
        Y = np.array([rewards.tolist()])
        self.model.fit(X, Y, verbose=False)
        if game_over:
            self.model.save_weights("saved-models/log_{}.h5".format(self.mark),
                                    overwrite=True)
