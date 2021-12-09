class Player:
    def __init__(self, name, color):
        self.name = name
        self._color = color
        self.startTile = None
        self.temporaryTiles = list()
        self._tilesBelong = list()

    def setupStartingBase(self, tile):
        self.startTile = tile

    def addTile(self, tile):
        self.clearLastSelectedTile()
        tile = self.__colorizeTile(tile)
        tile.setOccupied(True)
        tile.borderHardness = 4
        self.temporaryTiles.append(tile)

    def getTiles(self):
        return self._tilesBelong

    def clearLastSelectedTile(self):
        for tile in self.temporaryTiles:
            tile.setOccupied(False)
            tile.borderHardness = 1
            tile.setBorderColor((0, 0, 0))
        self.temporaryTiles.clear()

    def __colorizeTile(self, tile):
        tile.setBorderColor(self._color)
        return tile

    def commit(self):
        for tile in self.temporaryTiles:
            tile = self.__colorizeTile(tile)
            self._tilesBelong.append(tile)
        self.temporaryTiles.clear()
