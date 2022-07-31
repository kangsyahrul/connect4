import os

from model.point import Point


def clear_screen():
    # os.system('clear')
    os.system('cls' if os.name == 'nt' else 'clear')


def pixel_to_board_coordinate(px, py, padding, block_size):
    padding_x, padding_y = padding
    block_size_w, block_size_h = block_size
    return Point((px - padding_x) // block_size_w, (py - padding_y) // block_size_h)


def board_coordinate_to_pixel(point, padding, block_size):
    padding_x, padding_y = padding
    block_size_w, block_size_h = block_size
    x1, y1 = padding_x + point.x * block_size_w, padding_y + point.y * block_size_h
    x2, y2 = x1 + block_size_w, y1 + block_size_h
    return Point(x1, y1), Point(x2, y2)
