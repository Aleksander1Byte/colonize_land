import pygame
import sys
from generator import generate, create_map
from math import *
import numpy as np
from Exceptions import *

WINDOW_SIZE_X = 750
WINDOW_SIZE_Y = WINDOW_SIZE_X
FPS = 60
MAP_SIZE = 25
SEED = 100


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    heights = generate(SEED, MAP_SIZE)  # это должен вводить пользователь
    land = create_map(heights, (WINDOW_SIZE_X / MAP_SIZE) / sqrt(3))
    selectedTile = None

    glowingTiles = list()

    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                selectedTile = \
                    glow_border(event.pos[0], event.pos[1], land, selectedTile)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    ToFromTileManager('To', selectedTile, glowingTiles)
                    try:
                        print(glowingTiles[0][0].isBordering(glowingTiles[1][0]))
                    except AttributeError:
                        ToFromTileManager('From', selectedTile, glowingTiles)
                    except IndexError:
                        pass

                elif event.button == pygame.BUTTON_RIGHT:
                    ToFromTileManager('From', selectedTile, glowingTiles)

        for tile in glowingTiles:
            glow_border(*tile[0].Center, land, key=tile[1])

        draw_map(screen, land)
        pygame.display.flip()
    pygame.quit()


def ToFromTileManager(key, selectedTile, glowingTiles):
    """Принимает key от From до To, добавляет значение в glowingTiles"""
    for i in glowingTiles:
        if selectedTile is i[0]:
            return
    delGlowingTile(key, glowingTiles)
    glowingTiles.append([selectedTile, key])


def delGlowingTile(key, tiles):
    for ind, i in enumerate(tiles):
        if i[1] == key:
            tiles[ind][0].stopGlowing()
            del tiles[ind]
            return


def glow_border(x, y, land, PreviousTile=None, key='Selected'):
    """Подсвечивает границы тайла"""
    selectedTileIndex = getTileIndex(land, x, y)
    if PreviousTile is None:
        land[selectedTileIndex].startGlowing(key)
        return land[selectedTileIndex]
    else:
        PreviousTile.stopGlowing()
        land[selectedTileIndex].startGlowing(key)
        return land[selectedTileIndex]


def getTile(land, x, y):
    return land[getTileIndex(land, x, y)]


def getTileIndex(land, x, y):
    """Возвращает индекс тайла в массиве в зависимости от x и y"""
    list_of_difsX = np.array([abs(x - tile.center[0]) for tile in land])
    list_of_difsY = np.array([abs(y - tile.center[1]) for tile in land])
    return np.argmin(list_of_difsX + list_of_difsY)


def draw_map(screen, land):
    for tile in land:
        pygame.draw.polygon(screen, *tile.position)
        pygame.draw.lines(screen, *tile.borders)


if __name__ == '__main__':
    sys.exit(main())
