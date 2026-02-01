import curses
def main(window):
    global board_h, board_w, board

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_MAGENTA, -1)
    curses.init_pair(2, 237, -1)

    window = window

    board_h, board_w = 16, 16
    player = '██'
    player_x, player_y = board_w-1, board_h//2

    body = '##'
    snake_length = 1

    #               up     right    down    left
    directions = [(0, -1), (2, 0), (0, 1), (-2, 0)]
    current_rotation = -1

    window.refresh()

    board = curses.newwin(board_h, board_w*2, 2, 0)
    curses.curs_set(0)
    board.nodelay(True)
    board.keypad(True)
    board.box()


    background_dots()
    board.addstr(player_y, player_x, player, curses.color_pair(1))

    board.refresh()
    while True:
        key = board.getch()

        if key == ord('q'): return
        elif key == ord('w') and player_y>1: current_rotation = 0
        elif key == ord('s') and player_x<board_w*2-3: current_rotation = 1
        elif key == ord('r') and player_y<board_h-2: current_rotation = 2
        elif key == ord('a') and player_x>1: current_rotation = 3
        elif key == ord('p'):  # reset
            player_x, player_y = board_w-1, board_h//2
            current_rotation = -1
            snake_length = 1

            board.clear()
            background_dots()

        if current_rotation != -1:
            pass

        # board.addstr(0, 0, 'death')
        # board.refresh()
        # curses.napms(1500)
        # return

        window.addstr(0, 0, f'{(player_x, player_y)},  rotation: {current_rotation}, flag: ')
        # board.addstr(player_y, player_x, ' ·', curses.color_pair(2))

        window.refresh()
        board.refresh()

        curses.napms(500)

def background_dots():
    for i in range(1, board_h-1):
        for j in range(1, board_w * 2 - 1):
            if j % 2 == 0: board.addstr(i, j, "·", curses.color_pair(2))

curses.wrapper(main)