"""
main hub for our project
Initialises components and connects them
"""
import Game
import Model
import HumanPlayer
import Player
import statistics
import sys

game_count = 250000
epsilon = 1
steps = 0
eps_inter = 150
eps_change = 0.001
eps_min = 0

save_interval = 5000

statistic = statistics.Statistic(epsilon, game_count)

player_a_mark = 1
player_b_mark = 4


def main():
    args = sys.argv
    if len(args) == 1:
        learn()
    else:
        play()


def play():
    ai_player_mark = 1
    human_player_mark = 4

    ai_player = Player.Player(ai_player_mark, epsilon, True)
    human_player = HumanPlayer.HumanPlayer(human_player_mark)
    game = Game.GameManager(ai_player, human_player, statistic)


def learn():
    global epsilon
    global steps

    statistic.started()

    first_done = False

    model_a = Model.get_model()
    model_b = Model.get_model()

    for i in range(game_count):
        player_a = Player.Player(player_a_mark, epsilon, model_a)
        player_b = Player.Player(player_b_mark, epsilon, model_b)


        steps += 1
        #print("Game {} started".format(i))
        Game.GameManager(player_a, player_b, statistic)

        if steps % eps_inter == 0 and epsilon > eps_min:
            epsilon -= eps_change
            if epsilon < 0:
                epsilon = 0
            statistic.set_epsilon(epsilon)
            print("new epsilon: " + str(epsilon))

        if steps % save_interval == 0:
            model_a.model.save_weights("saved-models/log_1.h5")
            model_b.model.save_weights("saved-models/log_4.h5")
            statistic.print_statistic()
    statistic.ended()
    statistic.print_statistic()


if __name__ == "__main__":
    main()