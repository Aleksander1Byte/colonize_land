import sys

from generator import create_map
from math import sqrt
from player import Player
from tileManagment import *
from statistics import Statistics
from gameManager import *
from bot import Bot
from campaign import *
from secret import *
from menu import *


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
                if not player:
                    break
                name = player.split()[0]
                category = player.split()[1]
                color = list(map(int, player.split('(')[1][:-1].split(', ')))
                if category == 'bot':
                    player = Bot(name, color)
                else:
                    player = Player(name, color)
                players.append(player)
            except Exception as ex:
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
    secretPlayer = None
    endRect = None
    step = 0

    statistics = Statistics(WINDOW_SIZE_X, WINDOW_SIZE_Y, players)
    clock = pygame.time.Clock()

    menu, box = generateMenu(screen, WINDOW_SIZE_X)

    startGame(screen, WINDOW_SIZE_X)
    MenuSprite('menu/background/', 0, -70)
    addSpriteToMenuGroup(
        'menu/title/title.png', WINDOW_SIZE_X * .16, WINDOW_SIZE_Y * .017)
    addToGameplaySprites(
        'gameplay/scroll.png', WINDOW_SIZE_X * -.02, WINDOW_SIZE_X * .86)

    while running:
        if endGameFlag:
            if endRect:
                endRect = slideEnd(screen, WINDOW_SIZE_X, endRect, FPS)
            else:
                screen.fill('black')
            renderFinale(screen, players, WINDOW_SIZE_X)
            all_sprites.draw(screen)
            all_sprites.update()
        elif startGameFlag:
            screen.fill(pygame.Color('black'))
            draw_map(screen, land)
            gameplaySprites.draw(screen)
            statistics.draw(screen, step)
        else:
            menuGroup.draw(screen)
            menuGroup.update()
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
                if endGameFlag:
                    if event.key == pygame.K_RIGHT:
                        secretPlayer.move([10, 0])
                    if event.key == pygame.K_LEFT:
                        secretPlayer.move([-10, 0])
                    elif event.key == pygame.K_UP:
                        if secretPlayer.upDown:
                            secretPlayer.move([0, -10])
                    elif event.key == pygame.K_DOWN:
                        if secretPlayer.upDown:
                            secretPlayer.move([0, 10])
                if not startGameFlag:
                    if pygame.key.name(event.key).isdigit():
                        addNumToSeed(str(pygame.key.name(event.key)))
                    elif event.key == pygame.K_BACKSPACE:
                        delNumFromSeed()
                if event.key == pygame.K_SPACE:
                    step = commit(step)
                if event.key == pygame.K_n and pygame.key.get_mods()\
                        & pygame.KMOD_CTRL:
                    players[0].treasure = 10000
                if event.key == pygame.K_j and startGameFlag:
                    endGame(players)
                    if campaign:
                        heights = campaign.nextLevel()
                        if heights.any():
                            land = create_map(heights, sizeOfCell)
                            if not isinstance(defineWinners(players)[0][2],
                                              Bot) or all([isinstance(i, Bot)
                                                           for i in players]):
                                for player in players:
                                    player.getTiles().clear()
                                    player.treasure = 0
                                step = setupBots(land)
                                continue
                    endGameFlag = True
                    startGameFlag = False
                    endRect = [500, 0]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if endGameFlag:
                    if event.button == pygame.BUTTON_RIGHT:
                        if secretPlayer is None:
                            secretPlayer = SecretPlayer(event)
                        else:
                            secretPlayer.rect.x, secretPlayer.rect.y =\
                                event.pos
                    if event.button == pygame.BUTTON_LEFT and \
                            pygame.key.get_mods() & pygame.KMOD_CTRL:
                        Border(event, vertical=True)
                    elif event.button == pygame.BUTTON_LEFT:
                        Border(event)
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

        if not endGameFlag:
            for tile in glowingTiles:
                glow_border(*tile[0].Center, land, key=tile[1])

            for player in players:
                for tile in player.getTiles():
                    glow_border(*tile.Center, land)

        if players and not endGameFlag:
            if isinstance(players[step], Bot):
                players[step].turn()
                step = commit(step)
            else:
                players[step].drawTileWorth(screen, sizeOfCell)

        pygame.display.flip()
        clock.tick(FPS)
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
