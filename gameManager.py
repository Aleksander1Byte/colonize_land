import pygame
import thorpy


def generateMenu(screen, sizeOfScreen):
    exitButton = thorpy.make_button("Выйти из игры", func=thorpy.functions.quit_func)
    exitButton.set_size((sizeOfScreen * 0.73, sizeOfScreen * 0.07))
    box = thorpy.Box(elements=[exitButton])
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen
        box.set_topleft((sizeOfScreen * 0.12, sizeOfScreen * 0.12))
    return menu, box


def startGame(screen, sizeOfScreen):
    pygame.draw.rect(screen, pygame.Color('gray'), (sizeOfScreen * 0.1, sizeOfScreen * 0.1, sizeOfScreen * 0.8, sizeOfScreen * 0.9))


def endGame():
    pass
