import os
import sys

import pygame

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, event):
        super().__init__(all_sprites)
        self.image = pygame.Surface((20, 20))
        self.upDown = False
        self.vertical = False
        self.rect = pygame.Rect(*event.pos, 20, 20)
        pygame.draw.rect(self.image, (0, 0, 255), [0, 0, 20, 20])

        self.vy = 1.67

    def update(self):
        colliders = pygame.sprite.spritecollide(self, all_sprites, False)
        if len(colliders) == 1:
            self.rect = self.rect.move(0, self.vy)
        elif any(i.vertical for i in colliders[1:]):
            self.upDown = True
        else:
            self.upDown = False

    def move(self, velocity):
        if len(pygame.sprite.spritecollide(self, all_sprites, False)) != 1:
            self.rect = self.rect.move(*velocity)


class Border(pygame.sprite.Sprite):
    def __init__(self, event, vertical=False):
        super().__init__(all_sprites)
        self.vertical = vertical
        if self.vertical:
            self.add(vertical_borders)
            init = (10, 50)
            color = 'red'
        else:
            self.add(horizontal_borders)
            init = (50, 10)
            color = 'gray'
        self.image = pygame.Surface(init)
        self.rect = pygame.Rect(*event.pos, *init)
        pygame.draw.rect(self.image, pygame.Color(color),
                         (0, 0, init[0], init[1]))
