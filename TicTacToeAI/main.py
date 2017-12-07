"""
main hub for our project
Initialises components and connects them
"""
import Game
import HumanPlayer
import Player
import Visualizer
import statistics
import sys

game_count = 1000
epsilon = 1
steps = 0
eps_inter = 5
eps_change = 0.02

s = statistics.Statistic()

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
    game = Game.GameManager(ai_player, human_player, s)


def learn():
    global epsilon
    global steps
    player_a = Player.Player(player_a_mark, epsilon, False)
    player_b = Player.Player(player_b_mark, epsilon, False)
    s.started()
    print("Game 1 started")
    game = Game.GameManager(player_a, player_b, s)
    steps += 1
    for i in range(game_count):
        print("Game {} started".format(i))
        player_a = Player.Player(player_a_mark, epsilon, True)
        player_b = Player.Player(player_b_mark, epsilon, True)
        game = Game.GameManager(player_a, player_b, s)
        steps += 1
        if steps % eps_inter == 0 and epsilon > 0:
            epsilon -= eps_change
            print("new epsilon: " + str(epsilon))
    s.ended()
    s.print_statistic()


if __name__ == "__main__":
    main()