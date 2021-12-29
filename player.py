class Player:
    def __init__(self, name, color):
        self.name = name
        self._color = color
        self.startTile = None
        self.temporaryTiles = list()
        self.treasury = 0
        self.income = 0
        self._tilesBelong = set()

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

    def empireBorderingTiles(self):
        res = set()
        for tile in self._tilesBelong:
            for j in tile.borderingTiles:
                res.add(j)
        return res

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
            if not self._tilesBelong:
                self.setupStartingBase(tile)
            self._tilesBelong.add(tile)
        self.temporaryTiles.clear()

        self.income = sum(list(i.getWorth() for i in self._tilesBelong))
        self.treasury += self.income

    def drawTileWorth(self, screen, sizeOfCell):
        import pygame
        font = pygame.font.Font(None, 30)
        for tile in self._tilesBelong:
            line = str(tile.getWorth())
            x = tile.center[0] - sizeOfCell // 3
            y = tile.center[1] - sizeOfCell // 2
            text = font.render(str(line), True, self.getColor())
            screen.blit(text, (x, y))

    def getColor(self):
        return self._color
