import curses
from time import sleep
from time import monotonic
from random import randint

def main(stdscr):
    global window, start_x, start_y, board_height, board_width, \
        character_x, character_y, score, character, \
        apple, super_apple, ready

    window = stdscr

    character = 'x'
    apple = '@'
    super_apple = '$'

    ready = ''
    starting_menu()

    if ready == 'n':
        sleep(0.5)
        return

    curses.curs_set(0)
    window.keypad(True)
    curses.noecho()
    window.nodelay(True)

    start_x, start_y = 2, 3
    board_width, board_height = 16, 8

    character_x = start_x + board_width//2
    character_y = start_y + board_height//2
    score = 0

    apple_x, apple_y = generate_apple()

    super_apple_probability = 2
    super_apple_x, super_apple_y = 0, 0
    super_apple_chance = 0

    timer = 30.0
    previous_time = monotonic()
    while timer > 0:
        current_time = monotonic()
        time_difference = current_time - previous_time
        previous_time = current_time
        timer -= time_difference

        window.clear()
        print_board()
        print_leaderboard()

        window.addch(apple_y, apple_x, apple)
        if super_apple_chance == 1:
            window.addstr(super_apple_y, super_apple_x, super_apple)

        window.addstr(character_y, character_x, character)
        window.refresh()

        window.addstr(0, 0, f"Your Score: {score}")
        window.addstr(1, 0, f'Remaining Time: {timer: .2f}')

        global pressed_key
        pressed_key = window.getch()
        if pressed_key == ord('q'):
            window.clear()
            window.addstr(0, 0, 'thank you for playing the game')
            window.refresh()
            sleep(1)
            return
        move()

        if character_x == apple_x and character_y == apple_y:
            apple_x, apple_y = generate_apple()
            super_apple_chance = randint(1, super_apple_probability)
            if super_apple_chance == 1:
                super_apple_x, super_apple_y = generate_apple()
            score += 1
        if character_x == super_apple_x and character_y == super_apple_y:
            apple_x, apple_y = generate_apple()
            score += 10
            super_apple_chance = 0
            super_apple_x = super_apple_y = 0

        sleep(0.016)

    if timer <= 0: timeout_popup()

    window.nodelay(False)
    curses.echo()
    curses.curs_set(1)

    window.clear()

    name_prompt = 'Enter a name to save your score: '
    window.addstr(0, 0, f'Your Final Score: {score}')
    window.addstr(1, 0, name_prompt)
    window.addstr(2, 0, 'Leave name empty to quit without saving')
    window.refresh()

    name_bytes = window.getstr(1, len(name_prompt), 10)
    name = name_bytes.decode('utf-8')

    if name:
        save_score(name, score)

def starting_menu():
    curses.echo()
    global ready

    while ready != 'n' and ready != 'y':
        window.clear()
        window.addstr(0, 0, 'Welcome to Apple Eating Game')
        window.addstr(2, 0, f'{character} = player character. controlled using wasd or ↑←↓→.')
        window.addstr(3, 0, f'{apple} = basic apple. Gives 1 point.')
        window.addstr(4, 0, f'{super_apple} = Super apple. Gives 10 points.')
        window.addstr(5, 0, 'Press q to quit any time')

        ready_prompt = 'Ready to start? (y/n): '
        window.addstr(6, 0, ready_prompt)
        window.refresh()

        ready_byte = window.getstr(6, len(ready_prompt), 1)
        ready = ready_byte.decode('utf-8')

def print_board():
    window.addstr(start_y, start_x, f"+{'-' * board_width}+")
    window.addstr(start_y + 1 + board_height, start_x, f"+{'-' * board_width}+")
    for row in range(1, board_height + 1):
        window.addstr(start_y + row, start_x, f"|")
        window.addstr(start_y + row, start_x + board_width + 1, f"|")

def print_leaderboard():
    leaderboard_xlocation = start_x+board_width+4
    window.addstr(start_y, leaderboard_xlocation, 'Leaderboard (Top 10):')

    scores = []
    with open('scoreboard.txt') as file:
        scores = file.readlines()

    for player in range(10):
        try:
            window.addstr(start_y+1+player, leaderboard_xlocation, f'{scores[player].split()[0]:11s}{scores[player].strip().split()[1]}')
        except:
            print()

def move():
    global character_x, character_y

    if (pressed_key == ord('w') or pressed_key == curses.KEY_UP) and character_y > start_y + 1:
        character_y -= 1
    elif (pressed_key == ord('r') or pressed_key == curses.KEY_DOWN) and character_y < start_y + board_height:
        character_y += 1
    elif (pressed_key == ord('a') or pressed_key == curses.KEY_LEFT) and character_x > start_x + 1:
        character_x -= 1
    elif (pressed_key == ord('s') or pressed_key == curses.KEY_RIGHT) and character_x < start_x + board_width:
        character_x += 1

def save_score(name, score):
    scoreboard = open('scoreboard.txt', mode='a')
    scoreboard.write(f'{name}: {score}')
    scoreboard.close()
    sort_leaderboard()

def generate_apple():
    x = randint(start_x + 1, board_width + start_x)
    y = randint(start_y + 1, board_height + start_y)

    return x, y

def timeout_popup():
    popup_width, popup_height = 20, 5

    popup = curses.newwin(popup_height, popup_width, 2, start_x-1)
    popup.box()
    timeout_text = 'Time out!!'
    popup.addstr(popup_height//2, (popup_width-len(timeout_text))//2, timeout_text)
    popup.refresh()
    sleep(3)

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

curses.wrapper(main)