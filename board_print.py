import random

def create_board(width, height):
    global board_width, board_height, board
    board_width = width
    board_height = height

    board = [[' ' for _ in range(board_width)] for _ in range(board_height)]

def generate_random_1():
    random_width = random.randint(0, board_width-1)
    random_height = random.randint(0, board_height-1)

    board[random_height][random_width] = 'x'

    print(f'({random_width}, {random_height})')

def print_board():
    print(f'+{"-" * (board_width * 2 + 1)}+')
    for i in board:
        print('|', end=' ')
        for j in i: print(j, end=' ')
        print('|', end='')
        print()
    print(f'+{"-" * (board_width * 2 + 1)}+')

create_board(8, 10)
generate_random_1()
print_board()
