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
    model.add(Dense(1, input_shape=(19,), kernel_initializer='normal',
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
            #print("random action " + str(self.mark))
            self.action = random.randint(0, 8)
        else:
            #print("learned action " + str(self.mark))

            # get predicted action bla
            temp_gs = game_state.tolist()

            target = []
            target.extend(temp_gs)
            target.extend(temp_gs)
            target.append(-1)

            qvals = self.model.predict(np.array([target]))

            print("qvals for player {}:".format(self.mark))
            print(qvals)

            # prevent setting to middle segment on first move
            if first_move:
                qvals[0][4] = 0

            # get the action with the highest value
            self.action = np.argmax(qvals)
        callback(self.action, self.mark, self.reward_me)

    def reward_me(self, reward, new_game_state, game_over=False):
        # receive reward
        # receive new game state
        # save replay as [State, Action, NewState, Reward]
        self.log.append([self.game_state, self.action, new_game_state, reward])

        # TODO: use rewards for actual learning

        if game_over:
            target_log = []
            for i in range(len(self.log)):
                temp = []
                temp.extend(self.log[i][0]) # prior game state
                temp.extend(self.log[i][2]) # later game state
                temp.append(self.log[i][1]) # action
                target_log.append(temp)

            print(target_log)
            X = np.array(target_log)
            Y = np.array(self.log)[:, 3]

            print("X:")
            print(X.shape)

            for x in X:
                print(x)
                print("\n")
            print("Y:")
            print(Y)

            self.model.fit(X, Y)

        if self.step_counter % SAVE_INTERVAL == 0 or game_over:
            # t = datetime.datetime.now()
            self.model.save_weights('saved-models/log_{}.h5'
                                    .format(self.mark))



