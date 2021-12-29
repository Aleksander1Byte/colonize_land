from player import Player


tilesToChoose = ['Forest', 'Plains', 'Mountains', 'Sea', 'Desert']


class Bot(Player):
    def __init__(self, name, color):
        super(Bot, self).__init__(name, color)

    def turn(self):
        borderingTiles = [i for i in self.empireBorderingTiles()]
        sp = [i.getType() for i in borderingTiles]
        for i in tilesToChoose:
            while i in sp:
                ind = sp.index(i)
                bestTile = borderingTiles.pop(ind)
                sp.pop(ind)
                if bestTile not in self.getTiles() and\
                        bestTile.occupied == False:
                    self.addTile(bestTile)
                    return
