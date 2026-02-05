import curses
from time import sleep

def main(window):
    global board_h, board_w, board, player_x, player_y, \
        snake_length, current_rotation

    curses.start_color()
    curses.use_default_colors()
    window = window

    curses.init_pair(1, curses.COLOR_MAGENTA, -1)
    curses.init_pair(2, 237, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)

    board_h, board_w = 16, 16
    player = '██'
    player_x, player_y = board_w-1, board_h//2

    body = '██'
    snake_length = 3
    tail = [(player_x, player_y+(snake_length-i)) for i in range(1, snake_length)]

    #               up     right    down    left
    directions = [(0, -1), (2, 0), (0, 1), (-2, 0)]
    current_rotation = -1

    board = curses.newwin(board_h, board_w*2, 2, 0)
    curses.curs_set(0)
    board.nodelay(True)
    board.keypad(True)
    board.box()

    background_dots()
    board.addstr(player_y, player_x, player, curses.color_pair(1))

    window.refresh()
    board.refresh()
    while True:
        key = board.getch()

        if key == ord('q'): return
        elif key == ord('w'): current_rotation = 0
        elif key == ord('s'): current_rotation = 1
        elif key == ord('r'): current_rotation = 2
        elif key == ord('a'): current_rotation = 3
        elif key == ord('p'): reset()

        if current_rotation != -1:
            board.addstr(tail[0][1], tail[0][0], '  ')

            for i in range(0, snake_length-2):
                tail[i] = tail[i+1]

            tail[-1] = (player_x, player_y)
            player_x, player_y = player_x + directions[current_rotation][0], player_y + directions[current_rotation][1]

        if (player_x < 1 or player_x >= board_w*2-2) or (player_y < 1 or player_y >= board_h-1):
            board.addstr(0, 0, 'death')
            board.refresh()

            sleep(0.5)
            reset()

        for i in range(0, snake_length-1):
            board.addstr(tail[i][1], tail[i][0], body, curses.color_pair(3))
        board.addstr(player_y, player_x, player, curses.color_pair(1))
        window.addstr(0, 0, f'{(player_x, player_y)},  rotation: {current_rotation}    ')
        window.addstr(0, 0, f'tail: {tail}')

        window.refresh()
        board.refresh()

        curses.napms(500)

def background_dots():
    for i in range(1, board_h-1):
        for j in range(board_w * 2 - 1):
            if j % 2 != 0: board.addstr(i, j, "·", curses.color_pair(2))

def reset():
    global player_x, player_y, current_rotation, snake_length

    player_x, player_y = board_w - 1, board_h // 2
    current_rotation = -1
    snake_length = 1

    board.clear()
    board.box()
    background_dots()

curses.wrapper(main)