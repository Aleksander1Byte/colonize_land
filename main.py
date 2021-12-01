import pygame
import sys

WINDOW_SIZE_X = 500
WINDOW_SIZE_Y = 500
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color('white'))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
