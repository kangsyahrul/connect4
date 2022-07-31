import cv2
import numpy as np

from model.point import Point
import util.screen as sc

class Board:

    def __init__(self, window_size, padding, board_size, block_size):
        self.window_w, self.window_h = window_size
        self.padding_w, self.padding_h = padding
        self.board_w, self.board_h = board_size
        self.block_w, self.block_h = block_size

        self.value = self.create_board()
        self.shape = self.value.shape
        self.background = self.create_background()

        self.restart()

    def restart(self):
        self.value = self.create_board()

    def create_board(self):
        value = np.zeros((self.board_h, self.board_w), dtype=int)

        # value[self.board_h - 1 - 0][3] = 1
        # value[self.board_h - 1 - 0][2] = 1
        # value[self.board_h - 1 - 0][1] = 1
        # value[self.board_h - 1 - 0][0] = 1
        #
        # value[self.board_h - 1 - 0][0] = 1
        # value[self.board_h - 1 - 1][1] = 1
        # value[self.board_h - 1 - 2][2] = 1
        # value[self.board_h - 1 - 3][3] = 1
        #
        # value[0][0] = -1
        # value[1][1] = -1
        # value[2][2] = -1
        # value[3][3] = -1
        #
        # value[0][0] = -1
        # value[1][0] = -1
        # value[2][0] = -1
        # value[3][0] = -1

        return value

    def create_background(self):
        img = np.zeros((self.window_h, self.window_w, 3), dtype=np.uint8)

        x1, y1 = self.padding_w, self.padding_h
        x2, y2 = self.window_w - self.padding_w, self.window_h - self.padding_h

        img = cv2.rectangle(img, (x1, y1), (x2, y2), (222, 93, 23), -1)

        for x in range(self.board_w):
            for y in range(self.board_h):
                xc = self.padding_w + x * self.block_w + self.block_w // 2
                yc = self.padding_h + y * self.block_h + self.block_h // 2
                radius = int(((self.block_w // 2) + (self.block_h // 2)) // 2 * (1 - 0.2))

                val = self.value[y][x]

                color = (162, 72, 19)

                img = cv2.circle(img, (xc, yc), radius, color, -1)

        return img

    def draw_board(self):
        img = self.background.copy()

        for x in range(self.board_w):
            for y in range(self.board_h):
                val = self.value[y][x]
                if val == 0:
                    continue

                xc = self.padding_w + x * self.block_w + self.block_w // 2
                yc = self.padding_h + y * self.block_h + self.block_h // 2
                radius = int(((self.block_w // 2) + (self.block_h // 2)) // 2 * (1 - 0.2))

                color = (162, 72, 19)
                if val == 1:
                    color = (9, 9, 255)
                elif val == -1:
                    color = (83, 245, 255)

                img = cv2.circle(img, (xc, yc), radius, color, -1)

        return img

    def put_token(self, point, player):

        for y in range(self.board_h - 1, -1, -1):
            if self.value[y][point.x] == 0:
                self.value[y][point.x] = player
                return True
        return False

    def check_winner(self):
        is_game_over, winner, area = self.is_win('diagonal_up')
        if winner is not None:
            return is_game_over, winner, area

        is_game_over, winner, area = self.is_win('diagonal_down')
        if winner is not None:
            return is_game_over, winner, area

        is_game_over, winner, area = self.is_win('horizontal')
        if winner is not None:
            return is_game_over, winner, area

        is_game_over, winner, area = self.is_win('vertical')
        if winner is not None:
            return is_game_over, winner, area

        # Check if all array is full
        total_empty = np.sum(self.value == 0)
        if total_empty == 0:
            return True, None, []

        return False, None, []

    def is_win(self, mode):
        if mode == 'diagonal_up':
            x_start, x_inc = 0, +1
            y_start, y_inc = None, -1

        elif mode == 'diagonal_down':
            x_start, x_inc = self.board_w - 1, -1
            y_start, y_inc = None, -1

        elif mode == 'horizontal':
            x_start, x_inc = 0, +1
            y_start, y_inc = None, 0

        elif mode == 'vertical':
            x_start, x_inc = None, 0
            y_start, y_inc = 0, +1

        for i in range(self.board_w + self.board_h - 1):
            x = i if x_start is None else x_start
            y = i if y_start is None else y_start
            player, count, field = None, 0, []
            for j in range(self.board_w + self.board_h - 1):
                if 0 <= x < self.board_w and 0 <= y < self.board_h:
                    val = self.value[y][x]
                    if val == 0:
                        player, count, field = None, 0, []

                    else:
                        if val != player:
                            player = val
                            count = 1
                            field = [Point(x, y)]

                        else:
                            count += 1
                            field.append(Point(x, y))

                            if count >= 4:
                                return True, player, field

                x += x_inc
                y += y_inc

        return False, None, []

    def draw_winner(self, area):
        img = cv2.addWeighted(self.draw_board(), 0.3, np.zeros((self.window_h, self.window_w, 3), dtype=np.uint8), 1, 0)

        # Draw Tokens
        for point in area:
            val = self.value[point.y][point.x]
            if val == 0:
                continue

            xc = self.padding_w + point.x * self.block_w + self.block_w // 2
            yc = self.padding_h + point.y * self.block_h + self.block_h // 2
            radius = int(((self.block_w // 2) + (self.block_h // 2)) // 2 * (1 - 0.2))

            color = (162, 72, 19)
            if val == 1:
                color = (9, 9, 255)
            elif val == -1:
                color = (83, 245, 255)

            img = cv2.circle(img, (xc, yc), radius, color, -1)

        return img