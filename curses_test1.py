import curses
from time import sleep
from time import monotonic

def main(window):

    curses.curs_set(0)
    window.nodelay(True)

    x = 5
    y = 10

    timer = 5.0
    previous_time = monotonic()
    while timer > 0:

        current_time = monotonic()
        time_difference = current_time - previous_time
        previous_time = current_time
        timer -= time_difference

        window.clear()
        window.addstr(y, x, '@')
        window.refresh()

        window_height, window_width = window.getmaxyx()
        window.addstr(0, 0, f'({window_height}, {window_width})   ({y}, {x})')
        window.addstr(1, 0, f'remaining time: {timer}')

        pressed_key = window.getch()
        if pressed_key == ord('q'):
            window.addstr(0, 0, 'thank you for playing the game')
            window.refresh()
            sleep(1)
            break
        elif pressed_key == ord('w') and y > 0: y -= 1
        elif pressed_key == ord('r') and y < window_height-1: y += 1
        elif pressed_key == ord('a') and x > 0: x -= 1
        elif pressed_key == ord('s') and x < window_width-3: x += 1

        sleep(0.016)

    window.addstr(0, 0, 'time out!')
    window.refresh()
    sleep(3)

curses.wrapper(main)