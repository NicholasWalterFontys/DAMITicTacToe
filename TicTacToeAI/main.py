"""
main hub for our project
Initialises components and connects them
"""
import Player
import Game
import statistics

game_count = 150
epsilon = 1
steps = 0
eps_inter = 100
eps_change = 0.01

s = statistics.Statistic()

def main():
    global epsilon
    global steps
    player_a = Player.Player(1, epsilon, False)
    player_b = Player.Player(4, epsilon, False)
    game = Game.GameManager(player_a, player_b, s)
    steps += 1
    for i in range(game_count):
        player_a = Player.Player(1, epsilon, True)
        player_b = Player.Player(4, epsilon, True)
        game = Game.GameManager(player_a, player_b, s)
        steps += 1
        if steps % eps_inter == 0 and epsilon > 0:
            epsilon -= eps_change

    s.print_statistic()


if __name__ == "__main__":
    main()