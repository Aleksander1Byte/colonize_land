import pygame
import thorpy

pygame.init()
font = pygame.font.Font(None, 110)
SEED = ''


def generateMenu(screen, sizeOfScreen):
    startButton = thorpy.make_button("Начать игру",
                                     func=thorpy.constants.THORPY_EVENT)
    startButton.set_size((sizeOfScreen * 0.73, sizeOfScreen * 0.07))
    #  exitButton = thorpy.make_button("Выйти из игры",
    #                                  func=thorpy.functions.quit_func)
    #  exitButton.set_size((sizeOfScreen * 0.73, sizeOfScreen * 0.07))
    box = thorpy.Box(elements=[startButton])
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen
        box.set_topleft((sizeOfScreen * 0.12, sizeOfScreen * 0.12))
    return menu, box


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
                f'Оккупировано {len(i.getTiles()) / (MAP_SIZE ** 2 / 100)}%'
                f' континента\n\n')
    sp.sort(key=lambda x: x[1], reverse=True)
    print('Финальные результаты:')
    for i in range(len(players)):
        print(f'{i + 1} место - {sp[i][0]}, с результатом в {sp[i][1]} золота')


def addNumToSeed(num):
    global SEED
    if len(SEED) < 9:
        SEED += num


def delNumFromSeed():
    global SEED
    if len(SEED) > 0:
        SEED = SEED[:-1]
