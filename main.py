import pygame
import sys
from generator import generate
from math import *
from tile import Tile

WINDOW_SIZE_X = 750
WINDOW_SIZE_Y = WINDOW_SIZE_X
FPS = 60
MAP_SIZE = 25
SEED = 100


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    heights = generate(SEED, MAP_SIZE)  # это должен вводить пользователь
    land = create_map(heights, (WINDOW_SIZE_X / MAP_SIZE) / 1.5)
    while running:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_map(screen, land)
        pygame.display.flip()
    pygame.quit()


def draw_map(screen, land):
    for tile in land:
        pygame.draw.polygon(screen, *tile.position)
        pygame.draw.lines(screen, *tile.borders)


def create_map(heights, sizeOfcell):
    def calculate_point(center, size, i):
        angle_deg = 60 * i + 30
        angle_rad = pi / 180 * angle_deg
        return center[0] + size * cos(angle_rad),\
               center[1] + size * sin(angle_rad)

    shiftY = 0
    globalMap = list()
    for ind, i in enumerate(heights):
        if ind % 2 == 0:
            shiftX = 1
        else:
            shiftX = sqrt(3) / 2 * sizeOfcell
        for ind2, j in enumerate(i):
            points = list()
            for point in range(6):
                points.append(calculate_point(
                    [ind2 * sizeOfcell + shiftX,
                     ind * sizeOfcell + shiftY],
                    sizeOfcell, point))

            globalMap.append(Tile(j, points))
            shiftX += sizeOfcell / 2
        shiftY += sizeOfcell / 2
    return globalMap


if __name__ == '__main__':
    sys.exit(main())
