class Player:
    def __init__(self, name, color):
        self.name = name
        self._color = color
        self.startTile = None
        self._tilesBelong = list()

    def setupStartingBase(self, tile):
        self.startTile = tile

    def addTile(self, tile):
        tile = self.__colorizeTile(tile)
        tile.setOccupied(True)
        tile.borderHardness = 4
        self._tilesBelong.append(tile)

    def getTiles(self):
        return self._tilesBelong

    def __colorizeTile(self, tile):
        tile.setBorderColor(self._color)
        return tile
