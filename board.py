import pygame

import spritesheet
from piece import Type, Color, Piece


class Board:
    WHITE_COLOR = (238, 238, 210)
    BLACK_COLOR = (118, 150, 86)
    SELECT_COLOR = (246, 246, 105)
    TEXT_COLOR = (0, 0, 0)

    BOARD_NUMBERS = {8: 0, 7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7}
    BOARD_LETTERS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    NOTATION_TYPES = {'K': Type.KING, 'Q': Type.QUEEN, 'B': Type.BISHOP, 'N': Type.KNIGHT, 'R': Type.ROOK}

    START_WHITE_PIECES = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'Ra1', 'Nb1', 'Bc1', 'Qd1', 'Ke1', 'Bf1',
                          'Ng1', 'Rh1']
    START_BLACK_PIECES = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'Ra8', 'Nb8', 'Bc8', 'Qd8', 'Ke8', 'Bf8',
                          'Ng8', 'Rh8']

    def __init__(self, screen: 'Screen', square_size=64):
        self.square_size = square_size
        self.board_size = square_size * 8
        self.screen = screen
        self.center = self.board_size / 2
        self.start = (screen.center[0] - self.center, screen.center[1] - self.center)
        self.font = pygame.font.SysFont('Segoe UI Bold', 30)
        self.texts = []
        for i in self.BOARD_NUMBERS.keys():
            self.texts.append(self.font.render(str(i), False, self.TEXT_COLOR))
        for i in self.BOARD_LETTERS.keys():
            self.texts.append(self.font.render(i, False, self.TEXT_COLOR))

        spritesheet.load(square_size)

        self.pieces = [[None for i in range(8)] for j in range(8)]
        for p in self.START_WHITE_PIECES:
            self.create_piece_notation(p, Color.WHITE)
        for p in self.START_BLACK_PIECES:
            self.create_piece_notation(p, Color.BLACK)

        self.selected = None
        self.select_pos = None

    def draw(self):
        for i in range(64):
            x = i % 8
            y = i // 8

            if self.select_pos is not None and x == self.select_pos[0] and y == self.select_pos[1]:
                color = self.SELECT_COLOR
            elif y % 2 == 0:
                color = self.WHITE_COLOR if i % 2 == 0 else self.BLACK_COLOR
            else:
                color = self.WHITE_COLOR if i % 2 == 1 else self.BLACK_COLOR

            pos = self.get_square_pos(x, y)
            pygame.draw.rect(self.screen.display, color, (pos[0], pos[1], self.square_size, self.square_size))

        self.draw_texts()
        for x, r in enumerate(self.pieces):
            for y, p in enumerate(r):
                if p:
                    p.draw(x, y)

    def draw_texts(self):
        for y in range(8):
            pos = self.get_square_pos(-1, y)
            self.screen.display.blit(self.texts[y], (pos[0] + self.square_size / 2, pos[1] + self.square_size / 2))
        for x in range(8):
            pos = self.get_square_pos(x, 8)
            self.screen.display.blit(self.texts[8 + x], (pos[0] + self.square_size / 2, pos[1] + self.square_size / 4))

    def create_piece(self, x, y, piece_type: Type, color: Color):
        new_piece = Piece(piece_type, color, self)
        self.pieces[x][y] = new_piece
        return new_piece

    def create_piece_notation(self, notation, color: Color):
        if len(notation) == 3:
            piece_type = self.NOTATION_TYPES[notation[0]]
            x, y = self.square_from_notation(notation[1:])
        else:
            piece_type = Type.PAWN
            x, y = self.square_from_notation(notation)

        return self.create_piece(x, y, piece_type, color)

    def get_square_pos(self, x, y):
        return self.start[0] + x * self.square_size, self.start[1] + y * self.square_size

    def get_square_from_pos(self, x, y):
        return int((x - self.start[0]) // self.square_size), int((y - self.start[1]) // self.square_size)

    def square_from_notation(self, notation):
        letter = notation[0]
        number = int(notation[1])
        return self.BOARD_LETTERS[letter], self.BOARD_NUMBERS[number]

    def mouse_down(self, pos):
        x, y = self.get_square_from_pos(pos[0], pos[1])
        if self.selected:
            if self.pieces[x][y] is None or self.pieces[x][y].color == Color.BLACK:
                if self.can_move(x, y):
                    self.move_piece(x, y)
            else:
                self.selected = self.pieces[x][y]
                self.select_pos = (x, y)
        elif self.pieces[x][y] and self.pieces[x][y].color == Color.WHITE:
            self.selected = self.pieces[x][y]
            self.select_pos = (x, y)

    def can_move(self, x, y):
        piece = self.selected
        if piece.piece_type == Type.PAWN:
            if x == self.select_pos[0]:
                if self.select_pos[1] == 6:
                    if self.select_pos[1] - y <= 2:
                        return True
                else:
                    if self.select_pos[1] - y == 1:
                        return True

        return False

    def move_piece(self, x, y):
        self.pieces[x][y] = self.selected
        self.selected = None
        self.pieces[self.select_pos[0]][self.select_pos[1]] = None
        self.select_pos = None
