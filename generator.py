import numpy as np
from math import *
from tile import Tile

PERCENTAGE_OF_FLOOD = 0.1


def generate(seed, mapSize):
    """Создаётся массив с случайными числами, самые большие
     стремятся к центру массива, от этого генерируется карта, минимум 20% всех
      клеток по бокам будут морем"""
    np.random.seed(seed)
    mapSize += 1  # так как шестиугольники выходят за границу то без
    # прибавления получается mapSize - 0.5
    data = np.random.sample((mapSize, mapSize))
    data[mapSize // 2][mapSize // 2] = 1  # отмечаем центр карты
    for i in range(mapSize):
        for j in range(round(mapSize * PERCENTAGE_OF_FLOOD)):
            data[i][j] = 0.0
            data[i][mapSize - j - 1] = 0.0

    for i in range(round(mapSize * PERCENTAGE_OF_FLOOD)):
        for j in range(mapSize):
            data[i][j] = 0.0
            data[mapSize - i - 1][j] = 0.0
    return data


def create_map(heights, sizeOfcell):
    def calculate_point(center, size, i):
        angle_rad = radians(60 * i + 30)
        return center[0] + size * cos(angle_rad),\
               center[1] + size * sin(angle_rad)

    mapSize = len(heights)
    shiftY = sizeOfcell * 2 + sqrt(mapSize)
    globalMap = list()
    for ind, i in enumerate(heights):
        if ind % 2 == 0:
            shiftX = -3 - 15
        else:
            shiftX = sizeOfcell * 3/4 - 15
        for ind2, j in enumerate(i):
            points = list()
            centerX = ind2 * sizeOfcell + shiftX
            centerY = ind * sizeOfcell + shiftY
            for point in range(6):
                points.append(calculate_point(
                    [centerX, centerY],
                    sizeOfcell, point))

            globalMap.append(Tile(j, points, [centerX, centerY]))
            shiftX += sizeOfcell * 3/4 + 0.5
        shiftY += sizeOfcell / 2 + 0.5

    for ind, tile in enumerate(globalMap):
        try:
            tile.addBorderingTile(globalMap[ind - 1])
            tile.addBorderingTile(globalMap[ind + 1])
            tile.addBorderingTile(globalMap[ind - mapSize])
            tile.addBorderingTile(globalMap[ind + mapSize])
            if ind // mapSize % 2:
                tile.addBorderingTile(globalMap[ind - mapSize + 1])
                tile.addBorderingTile(globalMap[ind + mapSize + 1])
            else:
                tile.addBorderingTile(globalMap[ind - mapSize - 1])
                tile.addBorderingTile(globalMap[ind + mapSize - 1])
        except IndexError:
            pass

    return globalMap
