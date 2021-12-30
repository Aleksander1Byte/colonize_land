import sys

from generator import generate, create_map
from math import sqrt
from player import Player
from tileManagment import *
from statistics import Statistics
from gameManager import *
from bot import Bot
from campaign import *


def setupConfig():
    import configparser
    import os
    configParser = configparser.RawConfigParser()
    configFilePath = os.path.join('data/config.cfg')
    configParser.read(configFilePath)
    gameWidth = int(configParser.get("window", "Width"))
    fps = int(configParser.get("window", "FPS"))
    mapSize = int(configParser.get('gameplay', 'MapSize'))
    global WINDOW_SIZE_X, WINDOW_SIZE_Y, FPS, MAP_SIZE
    MAP_SIZE = mapSize
    FPS = fps
    WINDOW_SIZE_X = gameWidth
    WINDOW_SIZE_Y = WINDOW_SIZE_X + WINDOW_SIZE_X * 0.15


def setupPlayers():
    with open('data/PLAYERS.txt', 'r', encoding='utf8') as file:
        for _ in range(3):
            try:
                player = file.readline().rstrip()
                name = player.split()[0]
                category = player.split()[1]
                color = list(map(int, player.split('(')[1][:-1].split(', ')))
                if category == 'bot':
                    player = Bot(name, color)
                else:
                    player = Player(name, color)
                players.append(player)
            except Exception:
                print('Неправильно заданы игроки')
                exit()


WINDOW_SIZE_X: int
WINDOW_SIZE_Y: int
FPS: int
MAP_SIZE: int
SEED = 100
setupConfig()


players = list()
setupPlayers()
amountOfPlayers = len(players)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    SEED = 0
    heights = generate(SEED, MAP_SIZE)
    sizeOfCell = (WINDOW_SIZE_X / MAP_SIZE) / sqrt(3)
    land = create_map(heights, sizeOfCell)
    selectedTile = None
    glowingTiles = list()
    startGameFlag = False
    endGameFlag = False
    campaign = None
    step = 0

    statistics = Statistics(WINDOW_SIZE_X, WINDOW_SIZE_Y, players)

    menu, box = generateMenu(screen, WINDOW_SIZE_X)

    startGame(screen, WINDOW_SIZE_X)

    while running:
        if endGameFlag:
            if endRect:
                endRect = slideEnd(screen, WINDOW_SIZE_X, endRect, clock, FPS)
            else:
                screen.fill('black')
            renderFinale(screen, players, WINDOW_SIZE_X)
            pygame.display.flip()
        elif startGameFlag:
            screen.fill(pygame.Color('black'))
            draw_map(screen, land)
            statistics.draw(screen, step)
        else:
            drawSeed(screen, WINDOW_SIZE_X)
            box.blit()
            box.update()

        for event in pygame.event.get():
            if not startGameFlag and not endGameFlag:
                menu.react(event)

            if event == STARTCAMPAIGN:
                startGameFlag = True
                campaign = Campaign()
                sizeOfCell = (WINDOW_SIZE_X / 25) / sqrt(3)
                land = create_map(campaign.loadLevel(), sizeOfCell)
                step = setupBots(land)
                glowingTiles.clear()

            if event == STARTGAME:
                if startGameFlag:
                    continue
                startGameFlag = True
                from gameManager import SEED
                from random import choice
                if SEED == '':
                    from random import randint
                    SEED = randint(0, 1000)
                SEED = int(SEED)
                heights = generate(SEED, MAP_SIZE)
                sizeOfCell = (WINDOW_SIZE_X / MAP_SIZE) / sqrt(3)
                land = create_map(heights, sizeOfCell)
                step = setupBots(land)
                glowingTiles.clear()

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                selectedTile = \
                    glow_border(event.pos[0], event.pos[1], land, selectedTile)

            if event.type == pygame.KEYDOWN:
                if not startGameFlag:
                    if pygame.key.name(event.key).isdigit():
                        addNumToSeed(str(pygame.key.name(event.key)))
                    elif event.key == pygame.K_BACKSPACE:
                        delNumFromSeed()
                if event.key == pygame.K_SPACE:
                    step = commit(step)
                if event.key == pygame.K_j:
                    endGame(players)
                    if campaign:
                        heights = campaign.nextLevel()
                        if heights.any():
                            land = create_map(heights, sizeOfCell)
                            for player in players:
                                player.getTiles().clear()
                                step = setupBots(land)
                            continue
                    endGameFlag = True
                    startGameFlag = False
                    endRect = [500, 0]
                    clock = pygame.time.Clock()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if endGameFlag:
                    continue
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

        if players and not endGameFlag:
            players[step].drawTileWorth(screen, sizeOfCell)
            if isinstance(players[step], Bot):
                players[step].turn()
                step = commit(step)
        pygame.display.flip()
    pygame.quit()


def setupBots(land):
    from random import choice
    step = 0
    for bot in players:
        if isinstance(bot, Bot):
            tile = choice(land)
            while tile.getType() == 'Sea' or tile.occupied:
                tile = choice(land)
            bot.addTile(tile)
            step = commit(step)
    return step


def commit(step):
    players[step].commit()
    return (step + 1) % amountOfPlayers


def draw_map(screen, land):
    for tile in land:
        pygame.draw.polygon(screen, *tile.position)
        pygame.draw.lines(screen, *tile.borders)


if __name__ == '__main__':
    sys.exit(main())
