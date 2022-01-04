import thorpy
import pygame

pygame.init()
font = pygame.font.Font(None, 110)
STARTGAME = pygame.event.Event(pygame.USEREVENT + 1)
STARTCAMPAIGN = pygame.event.Event(pygame.USEREVENT + 2)


def start_Game():
    pygame.event.post(STARTGAME)


def start_Campaign():
    pygame.event.post(STARTCAMPAIGN)


def generateMenu(screen, sizeOfScreen):
    startButton = thorpy.make_button("Начать игру", func=start_Game)
    startButton.set_size((sizeOfScreen * 0.73, sizeOfScreen * 0.07))

    campaginButton = thorpy.make_button("Начать кампанию", func=start_Campaign)
    campaginButton.set_size((sizeOfScreen * 0.73, sizeOfScreen * 0.07))

    exitButton = thorpy.make_button("Выйти из игры",
                                    func=thorpy.functions.quit_func)
    exitButton.set_size((sizeOfScreen * 0.73, sizeOfScreen * 0.07))
    box = thorpy.Box(elements=[startButton, campaginButton, exitButton])
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen
        box.set_topleft((sizeOfScreen * 0.12, sizeOfScreen * 0.12))
    return menu, box
