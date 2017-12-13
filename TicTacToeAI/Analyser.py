import json
import matplotlib as plt

def convert():
    with open("log_1m.txt") as source:
        history = json.load(source)

    win_1_count = 0
    win_1_history = []
    win_4_count = 0
    win_4_history = []

    start_1_count = 0
    start_1_history = []
    start_4_count = 0
    start_4_history = []

    inv_moves_1_count = 0
    inv_moves_1_history = []
    inv_moves_4_count = 0
    inv_moves_4_history = []

    epsilon_history = []
    game_time_history = []

    for game in history:
        if game["winner"] == 1:
            win_1_count += 1
        elif game["winner"] == 4:
            win_4_count += 1

        if game["starter"] == 1:
            start_1_count += 1
        elif game["starter"] == 4:
            start_4_count += 1

        win_1_history.append(win_1_count)
        win_4_history.append(win_4_count)
        start_1_history.append(start_1_count)
        start_4_history.append(start_4_count)
        inv_moves_1_history.append(game["inv_moves_1"])
        inv_moves_4_history.append(game["inv_moves_4"])
        epsilon_history.append(game["epsilon"])
        game_time_history.append(game["game_time"])

    all_history = [win_1_history, win_4_history, start_1_history, start_4_history, inv_moves_1_history,
                           inv_moves_4_history, epsilon_history, game_time_history]

    with open("log_table.csv", "w") as target:
        target.write("sep=,\n")
        target.write("id,win_1,win_4,start_1,start_4,inv_mov_1,inv_mov_4,epsilon,game_time\n")
        for i in range(len(all_history[0])): # for all rows
            s = str(i) + ","
            for j in range(len(all_history)): # for all columns
                s += str(all_history[j][i])
                s += ","
            s = s[:-1]
            s += "\n"
            target.write(s)

def display():
    import numpy as np

    history = []
    with open("log_table_500k.csv") as source:
        lines = source.readlines()[2:] # skip first two lines
        for l in lines:
            split = l.split(",")
            for i in range(7):
                split[i] = int(split[i])
            for i in range(7,9):
                split[i] = float(split[i])
            history.append(split)
    history = np.array(history)

    print(history)

    from matplotlib import pyplot as plt

    fig = plt.figure(figsize=(11,8))
    ax1 = fig.add_subplot(111)
    ax1.set_ylim(0, 43)
    ax1.set_xlim(140000, 160000)

    ax1.plot(history[:, 5], label="Invalid moves player 1", color='r')
    ax1.plot(history[:, 6], label="Invalid moves player 4", color='g')
    ax1.plot(history[:, 7] * 100, label="Epsilon", color='b')

    plt.savefig("plot.png")


if __name__ == "__main__":
    #convert()
    display()