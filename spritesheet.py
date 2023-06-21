import pygame

PIECE_SPRITE_SIZE = 256
PIECES_SPRITE_SHEET = None


def load(square_size):
    global PIECES_SPRITE_SHEET
    PIECES_SPRITE_SHEET = pygame.image.load('sprites/pieces.png')
    scale_ratio = square_size / PIECE_SPRITE_SIZE
    width, height = PIECES_SPRITE_SHEET.get_width(), PIECES_SPRITE_SHEET.get_height()
    PIECES_SPRITE_SHEET = pygame.transform.scale(PIECES_SPRITE_SHEET,
                                                 (int(width * scale_ratio), int(height * scale_ratio)))
