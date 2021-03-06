import thorpy
import pygame
from data.imageManager import getAnimations, load_image

pygame.init()
font = pygame.font.Font(None, 110)
STARTGAME = pygame.event.Event(pygame.USEREVENT + 1)
STARTCAMPAIGN = pygame.event.Event(pygame.USEREVENT + 2)
menuGroup = pygame.sprite.Group()


class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, path, x=0, y=0):
        super().__init__(menuGroup)
        self.frames = getAnimations(path, True)
        self.frame = 0
        self.image = self.frames[self.frame]
        self.rect = pygame.Rect(x, y, self.image.get_width(),
                                self.image.get_height())
        self.subCounter = 0

    def update(self):
        if self.subCounter == 20:
            self.subCounter = 0
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]
        self.subCounter += 1


def addSpriteToMenuGroup(image, x, y, alpha=None):
    sprite = pygame.sprite.Sprite(menuGroup)
    image = load_image(image, alpha)
    sprite.image = image
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y


def start_Game():
    pygame.event.post(STARTGAME)


def start_Campaign():
    pygame.event.post(STARTCAMPAIGN)


def generateMenu(screen, sizeOfScreen):
    # http://thorpy.org/examples/image_buttons.html
    startButton = thorpy.make_button("Начать игру", func=start_Game)
    startButton.set_size((sizeOfScreen * 0.4, sizeOfScreen * 0.07))

    campaginButton = thorpy.make_button("Начать кампанию", func=start_Campaign)
    campaginButton.set_size((sizeOfScreen * 0.4, sizeOfScreen * 0.07))

    exitButton = thorpy.make_button("Выйти из игры",
                                    func=thorpy.functions.quit_func)
    exitButton.set_size((sizeOfScreen * 0.4, sizeOfScreen * 0.07))
    box = thorpy.Box(elements=[startButton, campaginButton, exitButton])
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen
        box.set_topleft((sizeOfScreen * 0.57, sizeOfScreen * 0.4))
    return menu, box
