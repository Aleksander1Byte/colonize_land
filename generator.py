import numpy as np
from random import randint


def generate(seed, mapSize):
    """Создаётся массив с случайными числами, самые большие
     стремятся к центру массива, от этого генерируется карта, минимум 20% всех клеток
     по бокам будут морем"""
    np.random.seed(seed)
    data = np.random.sample((mapSize, mapSize))
    data[len(data) // 2][len(data[0]) // 2] = 1  # отмечаем центр карты
    print(data)
    return data


generate(1000, 50)
