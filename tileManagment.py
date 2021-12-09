import numpy as np
from multipledispatch import dispatch
from tile import Tile


def ToFromTileManager(key, selectedTile, glowingTiles):
    """Принимает key от From до To, добавляет значение в glowingTiles"""
    delGlowingTile(key, glowingTiles)
    glowingTiles.append([selectedTile, key])


def isBusy(selectedTile, glowingTiles, players) -> bool:
    for i in players:
        if selectedTile in i.getTiles():
            return True
    for i in glowingTiles:
        if selectedTile is i[0]:
            return True
    return False


def delGlowingTile(key, tiles):
    for ind, i in enumerate(tiles):
        if i[1] == key:
            tiles[ind][0].stopGlowing()
            del tiles[ind]
            return


def glow_border(x, y, land, PreviousTile=None, key='Selected'):
    """Подсвечивает границы тайла"""
    selectedTileIndex = getTileIndex(land, x, y)
    try:
        PreviousTile.stopGlowing()
    except Exception:
        pass
    land[selectedTileIndex].startGlowing(key)
    return land[selectedTileIndex]


def getTile(land, x, y):
    return land[getTileIndex(land, x, y)]


def getTileIndex(land, x, y):
    """Возвращает индекс тайла в массиве в зависимости от x и y"""
    list_of_difsX = np.array([abs(x - tile.center[0]) for tile in land])
    list_of_difsY = np.array([abs(y - tile.center[1]) for tile in land])
    return np.argmin(list_of_difsX + list_of_difsY)
