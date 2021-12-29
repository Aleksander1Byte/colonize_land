import pygame
import sys
import thorpy

from generator import generate, create_map
from math import sqrt
from player import Player
from tileManagment import *
from statistics import Statistics
from gameManager import *

WINDOW_SIZE_X = 750
WINDOW_SIZE_Y = WINDOW_SIZE_X + WINDOW_SIZE_X * 0.15
FPS = 60
MAP_SIZE = 25
SEED = 100

players = [Player('Игрок1', (200, 0, 255)),
           Player('Бот1', (122, 122, 255))]  # Player('Бот1', (255, 0, 0))
amountOfPlayers = len(players)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    heights = generate(SEED, MAP_SIZE)  # это должен вводить пользователь
    sizeOfCell = (WINDOW_SIZE_X / MAP_SIZE) / sqrt(3)
    land = create_map(heights, sizeOfCell)
    selectedTile = None
    glowingTiles = list()
    startGameFlag = False
    step = 0

    statistics = Statistics(WINDOW_SIZE_X, WINDOW_SIZE_Y, players)
    print(f'Ход игрока {players[step].name}')

    menu, box = generateMenu(screen, WINDOW_SIZE_X)

    startGame(screen, WINDOW_SIZE_X)

    while running:
        if startGameFlag:
            screen.fill(pygame.Color('black'))
            draw_map(screen, land)
            statistics.draw(screen, step)
        else:
            box.blit()
            box.update()

        for event in pygame.event.get():
            if not startGameFlag:
                menu.react(event)

            if event.type == thorpy.THORPY_EVENT:
                startGameFlag = True
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                selectedTile = \
                    glow_border(event.pos[0], event.pos[1], land, selectedTile)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    step = commit(step)
                if event.key == pygame.K_j:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                empireTiles = players[step].empireBorderingTiles()
                if event.button == pygame.BUTTON_LEFT:
                    if selectedTile not in empireTiles and empireTiles:
                        break
                    if isBusy(selectedTile, glowingTiles, players):
                        break

                    ToFromTileManager('To', selectedTile, glowingTiles)
                    try:
                        if not empireTiles:
                            if glowingTiles[0][0].isBordering(
                                    glowingTiles[1][0]):
                                players[step].addTile(glowingTiles[1][0])
                            else:
                                players[step].clearLastSelectedTile()
                        else:
                            if glowingTiles[1][0] in empireTiles:
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

        players[step].drawTileWorth(screen, sizeOfCell)
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
