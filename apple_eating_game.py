import curses
from time import sleep

def main(window):
    curses.curs_set(0)

    start_x, start_y = 2, 2
    board_width, board_height = 16, 8

    character_x = start_x + board_width//2
    character_y = start_y + board_height//2

    while True:
        window.clear()

        window.addstr(start_y, start_x, f"+{'-'*board_width}+")
        window.addstr(start_y+1+board_height, start_x, f"+{'-'*board_width}+")
        for row in range(1, board_height+1):
            window.addstr(start_y+row, start_x, f"|")
            window.addstr(start_y+row, start_x+board_width+1, f"|")

        window.addstr(character_y, character_x, 'x')
        window.refresh()

        window.addstr(0, 0, f"({character_x}, {character_y})")

        pressed_key = window.getch()
        if pressed_key == ord('q'):
            window.addstr(0, 0, 'thank you for playing the game')
            window.refresh()
            sleep(1)
            break
        elif pressed_key == ord('w') and character_y > start_y+1:
            character_y -= 1
        elif pressed_key == ord('r') and character_y < start_y+board_height:
            character_y += 1
        elif pressed_key == ord('a') and character_x > start_x+1:
            character_x -= 1
        elif pressed_key == ord('s') and character_x < start_x+board_width:
            character_x += 1


curses.wrapper(main)