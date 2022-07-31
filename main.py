import cv2

from model.board import Board
from model.point import Point
import util.screen as sc

# GAME SETTING
BOARD_SIZE_W, BOARD_SIZE_H = BOARD_SIZE = (7, 6)

# SCREEN SETTING
WINDOW_TITLE = 'Connect4'
BLOCK_SIZE_W, BLOCK_SIZE_H = BLOCK_SIZE = (72, 72)
PADDING_X, PADDING_Y = PADDING = (24, 24)
WINDOW_SIZE_W, WINDOW_SIZE_H = WINDOW_SIZE = (PADDING_X * 2 + BOARD_SIZE_W * BLOCK_SIZE_W, PADDING_Y * 2 + BOARD_SIZE_H * BLOCK_SIZE_H)

USER, COMPUTER = 1, -1

board = Board(WINDOW_SIZE, PADDING, BOARD_SIZE, BLOCK_SIZE)
is_game_over = False
player = USER
winner = None
area = []


def mouse_callback(event, px, py, flags, param):
    global player, is_game_over, board, winner, area

    if event == cv2.EVENT_LBUTTONDOWN:
        if is_game_over:
            return

        # Convert to board coordinate
        point = sc.pixel_to_board_coordinate(px, py, PADDING, BLOCK_SIZE)
        is_valid = board.put_token(point, player)
        if is_valid:
            player = -player
            show_window()

        is_game_over, winner, area = board.check_winner()

        if is_game_over:
            game_over()

        # # User turn
        # move_possibilities, move_scores = board.get_possible_moves(player)
        # is_move_able = board.can_move(player)
        # if not is_move_able:
        #     is_game_over = True
        #     show_window()
        #
        # else:
        #     if player == USER:
        #         move_possibilities_list = list(chain.from_iterable(move_possibilities[y][x]))
        #         if True in move_possibilities_list:
        #             # print('Move: ', move_possibilities[y][x])
        #             # print('Count: ', move_possibilities_list.count(True))
        #             board.put_player(player, (x, y), move_possibilities[y][x])
        #             player = -player
        #             show_window()
        #
        #         # Computer turn
        #         (x, y), score = board.next_move(player)
        #         move_possibilities, move_scores = board.get_possible_moves(player)
        #         # print(f'Computer choice: {(x, y)}')
        #
        #         if None in [x, y]:
        #             is_game_over = True
        #             show_window()
        #
        #         else:
        #             board.put_player(player, (x, y), move_possibilities[y][x])
        #             player = -player
        #             show_window()
        #
        #             # User turn
        #             move_possibilities, move_scores = board.get_possible_moves(player)
        #             is_move_able = board.can_move(player)
        #             if not is_move_able:
        #                 is_game_over = True
        #                 show_window()


def show_window(img=None):
    if img is None:
        img = board.draw_board()
    cv2.imshow(WINDOW_TITLE, img)


def game_over():
    global winner, area

    if len(area) > 0:
        img = board.draw_winner(area)
        show_window(img)

    sc.clear_screen()
    print(f'Press "R" to rematch/restart')
    print(f'Press "Q" to quit the game')
    print()
    print('GAME OVER')
    print(f'Winner: {winner}')


def rematch():
    global is_game_over, winner, player, area
    is_game_over, winner, player, area = False, None, USER, []

    board.restart()
    show_window()

    sc.clear_screen()
    print(f'Press "R" to rematch/restart')
    print(f'Press "Q" to quit the game')
    print()


def main():
    cv2.namedWindow(WINDOW_TITLE)
    cv2.setMouseCallback(WINDOW_TITLE, mouse_callback)

    rematch()
    while True:
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

        if key == ord('r'):
            rematch()

    print('Exit the game')


if __name__ == '__main__':
    main()
