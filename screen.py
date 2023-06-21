import pygame
import board


class Screen:
    BACKGROUND = (49, 46, 43)

    def __init__(self, size=(1000, 1000)):
        self.size = size
        self.center = (self.size[0] / 2, self.size[1] / 2)
        self.display = pygame.display.set_mode(size)
        pygame.display.set_caption("Chess Engine")
        self.board = board.Board(self)

    def draw(self):
        self.display.fill(self.BACKGROUND)
        self.board.draw()
        pygame.display.flip()

    def mouse_down(self, pos):
        x, y = pos
        if x < self.board.start[0]:
            return
        elif y < self.board.start[1]:
            return
        elif x > self.board.start[0] + self.board.board_size:
            return
        elif y > self.board.start[1] + self.board.board_size:
            return
        self.board.mouse_down(pos)
