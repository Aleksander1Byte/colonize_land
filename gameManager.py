import pygame
from menu import font

SEED = ''


def startGame(screen, sizeOfScreen):
    pygame.draw.rect(screen, pygame.Color('gray'),
                     (sizeOfScreen * 0.1, sizeOfScreen * 0.1,
                      sizeOfScreen * 0.8, sizeOfScreen * 0.9))


def drawSeed(screen, sizeOfScreen):
    pygame.draw.rect(screen, pygame.Color('black'),
                     (sizeOfScreen * 0.2, sizeOfScreen * 0.8,
                      sizeOfScreen * 0.6, sizeOfScreen * 0.1))
    text = font.render(SEED, False, (100, 255, 100))
    screen.blit(text, (sizeOfScreen * 0.2, sizeOfScreen * 0.8))


def defineWinners(players):
    sp = list()
    for i in players:
        sp.append([i.name, i.treasure, i])
    sp.sort(key=lambda x: x[1], reverse=True)
    return sp


def endGame(players):
    from main import MAP_SIZE
    sp = list()
    with open('Statistics.txt', 'w', encoding='utf8') as file:
        for i in players:
            sp.append([i.name, i.treasure])
            file.write(f"{i.name}: \n")
            file.write(f'Накопил {i.treasure} золота\n')
            file.write(f'Завоевал {len(i.getTiles())} клеток\n')
            file.write(
                f'Оккупировано '
                f'{round(len(i.getTiles()) / ((MAP_SIZE + 1) ** 2 / 100), 2)}%'
                f' карты\n\n')
    sp.sort(key=lambda x: x[1], reverse=True)
    print('Финальные результаты:')
    for i in range(len(players)):
        print(f'{i + 1} место - {sp[i][0]}, с результатом в {sp[i][1]} золота')


def renderFinale(screen, players, sizeOfScreen):
    sp = list()
    font = pygame.font.Font(None, 50)
    for i in players:
        sp.append([i.name, i.treasure])
    sp.sort(key=lambda x: x[1], reverse=True)
    for i in range(len(players)):
        color = (255, 215, 0) if not i else (197, 201, 199)\
            if i == 1 else (205, 127, 50) if i == 2 else (255, 255, 255)
        line = f'{i + 1} место - {sp[i][0]}'
        text = font.render(line, True, color)
        screen.blit(text, (sizeOfScreen * 0.05, sizeOfScreen * 0.2 + 200 * i))
        line = f'{sp[i][1]} золота'
        text = font.render(line, True, color)
        screen.blit(text, (sizeOfScreen * 0.05,
                           sizeOfScreen * 0.2 + 200 * i + 70))


def slideEnd(screen, sizeOfScreen, cords, fps):
    if not cords:
        return
    if cords == [500, 0]:
        cords[0] = -sizeOfScreen
    if cords[0] > 0:
        return False
    pygame.draw.rect(
        screen, (0, 0, 0), (cords[0], cords[1], sizeOfScreen + 5,
                            sizeOfScreen + sizeOfScreen * 0.15))
    cords[0] += 500 / fps
    return cords


def addNumToSeed(num):
    global SEED
    if len(SEED) < 9:
        SEED += num


def delNumFromSeed():
    global SEED
    if len(SEED) > 0:
        SEED = SEED[:-1]
