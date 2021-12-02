import pygame


colors = {'Sea': pygame.Color('blue'), 'Plains': pygame.Color('green'),
              'Desert': pygame.Color('#fcdd76'),
              'Mountains': pygame.Color('white'),
              'Forest': pygame.Color('#0a5f38')}


class Tile:
    def __init__(self, j, cords):
        self.height = j
        self.cords = cords
        print(self.cords)
        self.__initTile()

    def __initTile(self):
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

    @property
    def position(self):
        return self.color, self.cords

    @property
    def borders(self):
        return (0, 0, 0), False, self.cords, 1
