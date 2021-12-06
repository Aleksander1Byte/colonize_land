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

    def isBordering(self, tile):
        return True if tile in self.__borderingTiles else False

    def startGlowing(self, key='Selected'):
        self.borderColor = colors[key]
        self.borderHardness = 2

    def stopGlowing(self):
        self.borderColor = colors['Border']
        self.borderHardness = 1

    def isGlowing(self):
        return True if self.borderHardness == 2 else False

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

