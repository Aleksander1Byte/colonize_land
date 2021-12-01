import pygame
import sys
from generator import generate
from math import *

WINDOW_SIZE_X = 500
WINDOW_SIZE_Y = 500
FPS = 60
MAP_SIZE = 25
SEED = 100


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    pygame.display.set_caption('Колонизация')
    running = True
    land = generate(SEED, MAP_SIZE)  # это должен вводить пользователь
    while running:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_map(screen, land, WINDOW_SIZE_X / (MAP_SIZE + MAP_SIZE / 2))
        pygame.display.flip()
    pygame.quit()


def draw_map(screen, land, sizeOfcell):
    sizeOfcell = round(sizeOfcell)

    def calculate_point(center, size, i):
        angle_deg = 60 * i + 30
        angle_rad = pi / 180 * angle_deg
        return center[0] + size * cos(angle_rad),\
               center[1] + size * sin(angle_rad)

    colors = [pygame.Color('blue'), pygame.Color('green'),
              pygame.Color('#fcdd76'), pygame.Color('white')]

    shiftY = 0
    for ind, i in enumerate(land):
        if ind % 2 == 0:
            shiftX = 0
        else:
            shiftX = sqrt(3) / 2 * (sizeOfcell * 2) / 2
        for ind2, j in enumerate(i):
            if j < 0.15:
                color = colors[0]
            elif j < 0.3:
                color = colors[2]
            elif j > 0.95:
                color = colors[3]
            else:
                color = colors[1]
            points = list()
            for point in range(6):
                points.append(calculate_point(
                    [ind2 * sizeOfcell + shiftX,
                     ind * sizeOfcell + shiftY],
                    sizeOfcell, point))

            pygame.draw.polygon(screen, color, points)
            pygame.draw.lines(screen, (0, 0, 0), False, points, 1)
            shiftX += sizeOfcell / 2
        shiftY += sizeOfcell / 2


if __name__ == '__main__':
    sys.exit(main())
