"""
main hub for our project
Initialises components and connects them
"""
import Player
import Game
import statistics

game_count = 10
epsilon = 1
steps = 0
eps_inter = 100
eps_change = 0.01

s = statistics.Statistic()

player_a_mark = 1
player_b_mark = 4


def main():
    global epsilon
    global steps
    player_a = Player.Player(player_a_mark, epsilon, False)
    player_b = Player.Player(player_b_mark, epsilon, False)
    game = Game.GameManager(player_a, player_b, s)
    steps += 1
    for i in range(game_count):
        player_a = Player.Player(player_a_mark, epsilon, True)
        player_b = Player.Player(player_b_mark, epsilon, True)
        game = Game.GameManager(player_a, player_b, s)
        steps += 1
        if steps % eps_inter == 0 and epsilon > 0:
            epsilon -= eps_change

    s.print_statistic()


if __name__ == "__main__":
    main()