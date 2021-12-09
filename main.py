import pygame
import sys
from generator import generate, create_map
from math import *
import numpy as np
from player import Player
from tileManagment import *

WINDOW_SIZE_X = 750
WINDOW_SIZE_Y = WINDOW_SIZE_X
FPS = 60
MAP_SIZE = 25
SEED = 100

players = [Player('Игрок1', (200, 0, 255)), Player('Бот1', (255, 0, 0))]
amountOfPlayers = len(players)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    heights = generate(SEED, MAP_SIZE)  # это должен вводить пользователь
    land = create_map(heights, (WINDOW_SIZE_X / MAP_SIZE) / sqrt(3))
    selectedTile = None
    glowingTiles = list()
    step = 0

    print(f'Ход игрока {players[step].name}')
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                selectedTile = \
                    glow_border(event.pos[0], event.pos[1], land, selectedTile)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    step = commit(step)
                    print(f'Ход игрока {players[step].name}')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if isBusy(selectedTile, glowingTiles, players):
                    break
                if event.button == pygame.BUTTON_LEFT:
                    ToFromTileManager('To', selectedTile, glowingTiles)
                    try:
                        if glowingTiles[0][0].isBordering(glowingTiles[1][0]):
                            players[step].addTile(glowingTiles[1][0])
                        else:
                            players[step].clearLastSelectedTile()

                    except AttributeError:
                        ToFromTileManager('From', selectedTile, glowingTiles)
                    except IndexError:
                        pass

                elif event.button == pygame.BUTTON_RIGHT:
                    ToFromTileManager('From', selectedTile, glowingTiles)

        for tile in glowingTiles:
            glow_border(*tile[0].Center, land, key=tile[1])

        for player in players:
            for tile in player.getTiles():
                glow_border(*tile.Center, land)

        draw_map(screen, land)
        pygame.display.flip()
    pygame.quit()


def commit(step):
    players[step].commit()
    return (step + 1) % amountOfPlayers


def draw_map(screen, land):
    for tile in land:
        pygame.draw.polygon(screen, *tile.position)
        pygame.draw.lines(screen, *tile.borders)


if __name__ == '__main__':
    sys.exit(main())
