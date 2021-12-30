from generator import generate
levels = {1: generate(10000, 25, 0.17), 2: generate(2542, 25, 0.24),
          3: generate(1441, 25, 0.3)}


class Campaign:
    def __init__(self, startLevel=1):
        self.level = startLevel

    def loadLevel(self, levelID=None):
        if levelID is None:
            levelID = self.level
        level = levels[levelID]
        return level

    def nextLevel(self):
        if self.level < 3:
            self.level += 1
            return self.loadLevel()
        from numpy import array
        return array(0)

