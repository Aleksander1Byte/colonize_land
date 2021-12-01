import numpy as np

PERCENTAGE_OF_FLOOD = 0.1


def generate(seed, mapSize):
    """Создаётся массив с случайными числами, самые большие
     стремятся к центру массива, от этого генерируется карта, минимум 20% всех
      клеток по бокам будут морем"""
    np.random.seed(seed)
    mapSize += 2  # так как шестиугольники выходят за границу то без
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
