from enum import IntEnum

import spritesheet


class Type(IntEnum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5


class Color(IntEnum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, piece_type: Type, color: Color, board):
        self.sprite_offset = (int(piece_type) * board.square_size, int(color) * board.square_size)
        self.piece_type = piece_type
        self.color = color
        self.board = board

    def draw(self, x, y):
        pos = self.board.get_square_pos(x, y)
        self.board.screen.display.blit(spritesheet.PIECES_SPRITE_SHEET, (pos[0], pos[1]),
                                       (self.sprite_offset[0], self.sprite_offset[1], self.board.square_size,
                                        self.board.square_size))
