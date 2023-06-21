import pygame

from screen import Screen
pygame.init()
pygame.font.init()

screen = Screen()
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            screen.mouse_down(pos)

    screen.draw()
    clock.tick(60)

pygame.quit()
