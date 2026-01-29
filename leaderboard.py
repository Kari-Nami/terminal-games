
def sort_leaderboard():

    file = open('scoreboard.txt')
    scores = file.readlines()
    file.close()

    for i in range(len(scores)):
        scores[i] = scores[i].split()
        scores[i][1] = int(scores[i][1])

    scores.sort(key=lambda x: x[1], reverse=True)

    with open('scoreboard.txt', 'w') as file:
        for row in scores:
            file.write(f'{row[0]} {row[1]}\n')

sort_leaderboard()
