import sys
import os
import pygame


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


def getAnimations(path, background=False):
    """Возвращает список кадров"""
    arg = None
    if not background:
        arg = -1
    files = os.listdir('data/' + path)
    sp = list()
    for i in range(len(files)):
        sp.append(load_image(path + files[i], arg))
    return sp
