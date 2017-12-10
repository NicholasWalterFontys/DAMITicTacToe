from keras.models import Sequential
from keras.layers.core import *
from keras.optimizers import RMSprop

instance_a = None
instance_b = None


def get_instance_a(path=None):
    """
    get singleton instance a
    :param path: path to load saved weights from, leave empty to start blank
    :return: None
    """
    global instance_a

    if instance_a is None:
        instance_a = ModelContainer(path)
    return instance_a


def get_instance_b(path=None):
    """
    get singleton instance b
    :param path: path to load saved weights from, leave empty to start blank
    :return: None
    """
    global instance_b

    if instance_b is None:
        instance_b = ModelContainer(path)
    return instance_b


def get_model(path=None):
    return ModelContainer(path)

class ModelContainer:
    def __init__(self, path_to_load=None):
        """
        initialises the Sequential model
        :param path_to_load:
        """
        self.model = Sequential()

        # input size of 9 (rewards for each possible move)
        # output size of 9 (q values for each possible move)
        self.model.add(Dense(9, input_dim=9,
                             kernel_initializer='normal',
                             activation='relu'))
        self.model.compile(loss='mse', optimizer=RMSprop())

        if path_to_load is not None:
            self.model.load_weights(path_to_load)
