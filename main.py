import pygame
import sys
from generator import generate

WINDOW_SIZE_X = 500
WINDOW_SIZE_Y = 500
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    land = generate(100, 50)
    while running:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_map(screen, land, WINDOW_SIZE_Y // 50)
        pygame.display.flip()
    pygame.quit()


def draw_map(screen, land, sizeOfcell):
    colors = [pygame.Color('blue'), pygame.Color('green')]
    for ind, i in enumerate(land):
        for ind2, j in enumerate(i):
            pygame.draw.rect(screen, colors[0] if j < 0.3 else colors[1],
                             (ind2 * sizeOfcell, ind * sizeOfcell, sizeOfcell,
                              sizeOfcell))


if __name__ == '__main__':
    sys.exit(main())
