import pygame


colors = {'Sea': pygame.Color('blue'), 'Plains': pygame.Color('green'),
              'Desert': pygame.Color('#fcdd76'),
              'Mountains': pygame.Color('white'),
              'Forest': pygame.Color('#0a5f38'),
          'Selected': (0, 191, 255), 'Border': (0, 0, 0),
          'From': (255, 0, 0), 'To': (255, 255, 0)}


class Tile:
    def __init__(self, j, cords, center):
        self.height = j
        self.cords = cords
        self.Center = center
        self.borderHardness = 1
        self.occupied = False
        self.__borderingTiles = list()
        self.__initTile()

    def __initTile(self):
        self.borderColor = colors['Border']
        if self.height < 0.15:  # море
            self.__type = 'Sea'
        elif self.height < 0.3:  # пустыня
            self.__type = 'Desert'
        elif self.height < 0.4:  # пустыня
            self.__type = 'Forest'
        elif self.height > 0.95:  # горы
            self.__type = 'Mountains'
        else:  # равнина
            self.__type = 'Plains'
        self.color = colors[self.__type]

    def addBorderingTile(self, tile):
        self.__borderingTiles.append(tile)

    @property
    def borderingTiles(self):
        return self.__borderingTiles

    def setBorderColor(self, color):
        self.borderColor = color

    def isBordering(self, tile):
        return True if tile in self.__borderingTiles else False

    def setOccupied(self,  val=True):
        self.occupied = val

    def startGlowing(self, key='Selected', hardness=2):
        if key is None or self.occupied:
            return
        self.borderHardness = hardness
        self.borderColor = colors[key]

    def stopGlowing(self):
        if self.occupied:
            return
        self.borderColor = colors['Border']
        self.borderHardness = 1

    def isGlowing(self):
        return True if self.borderHardness != 1 else False

    def getType(self):
        return self.__type

    @property
    def position(self):
        return self.color, self.cords

    @property
    def coordinates(self):
        return self.cords

    @property
    def borders(self):
        return self.borderColor, True, self.cords, self.borderHardness

    @property
    def center(self):
        return self.Center

