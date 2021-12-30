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


class SecretPlayer(pygame.sprite.Sprite):
    def __init__(self, event):
        super().__init__(all_sprites)
        self.frames = []
        self.cur_frame = 0
        self.subCur_frame = 0
        self.idleLFrames = self.openAnim('idle_/')
        self.idleRFrames = self.openAnim('idle2_/')
        self.fallFrames = self.openAnim('fall_/')
        self.runRFrames = self.openAnim('walkLRun_/')
        self.runLFrames = self.openAnim('walkRRun_/')

        self.frames = self.idleLFrames
        self.image = self.frames[self.cur_frame]
        self.upDown = False
        self.vertical = False
        self.rect = pygame.Rect(0, 0, self.image.get_width(),
                                self.image.get_height())
        self.rect = self.rect.move(*event.pos)
        self.lastMovement = 0
        self.vy = 1.67

    def openAnim(self, path):
        files = os.listdir('data/' + path)
        sp = list()
        for i in range(len(files)):
            sp.append(load_image(path + files[i], -1))
        return sp

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.lastMovement = [0, 0]
        if self.subCur_frame >= 3:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.subCur_frame = 0
        else:
            self.subCur_frame += 1
        try:
            self.image = self.frames[self.cur_frame]
        except IndexError:
            self.image = self.frames[-1]
        colliders = pygame.sprite.spritecollide(self, all_sprites, False)
        if len(colliders) == 1:
            self.rect = self.rect.move(0, self.vy)
            self.checkAnim((0, self.vy))
            self.lastMovement = (0, self.vy)
        elif any(i.vertical for i in colliders[1:]):
            self.upDown = True
        else:
            self.upDown = False

    def checkAnim(self, velocity):
        if velocity[0] > 0:
            self.frames = self.runRFrames
        if velocity[0] < 0:
            self.frames = self.runLFrames
        if velocity[1] > 0:
            self.frames = self.fallFrames
            self.subCur_frame += 3
        else:
            if self.frames == self.runRFrames:
                self.frames = self.idleRFrames
            else:
                self.frames = self.idleLFrames

    def move(self, velocity):
        if len(pygame.sprite.spritecollide(self, all_sprites, False)) != 1:
            self.checkAnim(velocity)
            self.lastMovement = velocity
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
