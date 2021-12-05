import pygame
import sys
from generator import generate, create_map
from math import *
import numpy as np
from Exceptions import *

WINDOW_SIZE_X = 750
WINDOW_SIZE_Y = WINDOW_SIZE_X + WINDOW_SIZE_X // 15
FPS = 60
MAP_SIZE = 20
SEED = 100


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    heights = generate(SEED, MAP_SIZE)  # это должен вводить пользователь
    land = create_map(heights, (WINDOW_SIZE_X / MAP_SIZE) / sqrt(3))
    selectedTile = None
    tileFrom = None

    while running:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                selectedTile = \
                    glow_border(event.pos[0], event.pos[1], land, selectedTile)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    tileTo = selectedTile
                    try:
                        print(tileFrom.isBordering(tileTo))
                    except AttributeError:
                        tileFrom = selectedTile
                elif event.button == pygame.BUTTON_RIGHT:
                    tileFrom = selectedTile

        draw_map(screen, land)
        pygame.display.flip()
    pygame.quit()


def glow_border(x, y, land, selectedTile):
    list_of_difsX = np.array([abs(x - tile.center[0]) for tile in land])
    list_of_difsY = np.array([abs(y - tile.center[1]) for tile in land])
    selectedTileIndex = np.argmin(list_of_difsX + list_of_difsY)
    if selectedTile is None:
        land[selectedTileIndex].startGlowing()
        return land[selectedTileIndex]
    else:
        selectedTile.stopGlowing()
        land[selectedTileIndex].startGlowing()
        return land[selectedTileIndex]


def draw_map(screen, land):
    for tile in land:
        pygame.draw.polygon(screen, *tile.position)
        pygame.draw.lines(screen, *tile.borders)


if __name__ == '__main__':
    sys.exit(main())
