import pygame


colors = {'Sea': pygame.Color('blue'), 'Plains': pygame.Color('green'),
              'Desert': pygame.Color('#fcdd76'),
              'Mountains': pygame.Color('white'),
              'Forest': pygame.Color('#0a5f38'),
          'Glow': (0, 191, 255), 'Border': (0, 0, 0)}


class Tile:
    def __init__(self, j, cords, center):
        self.height = j
        self.cords = cords
        self.Center = center
        self.borderHardness = 1
        self.__initTile()

    def __initTile(self):
        self.borderColor = colors['Border']
        if self.height < 0.15:  # море
            self.name = 'Sea'
        elif self.height < 0.3:  # пустыня
            self.name = 'Desert'
        elif self.height < 0.4:  # пустыня
            self.name = 'Forest'
        elif self.height > 0.95:  # горы
            self.name = 'Mountains'
        else:  # равнина
            self.name = 'Plains'
        self.color = colors[self.name]

    def startGlowing(self):
        self.borderColor = colors['Glow']
        self.borderHardness = 2

    def stopGlowing(self):
        self.borderColor = colors['Border']
        self.borderHardness = 1

    @property
    def position(self):
        return self.color, self.cords

    @property
    def stats(self):
        return self.height, self.cords, self.Center

    @property
    def coordinates(self):
        return self.cords

    @property
    def borders(self):
        return self.borderColor, False, self.cords, self.borderHardness

    @property
    def center(self):
        return self.Center

