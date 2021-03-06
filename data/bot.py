from data.player import Player


tilesToChoose = ['Forest', 'Plains', 'Mountains', 'Sea', 'Desert']


class Bot(Player):
    def __init__(self, name, color):
        super(Bot, self).__init__(name, color)

    def turn(self):
        from random import randint
        if not randint(0, 20):
            return
        borderingTiles = [i for i in self.empireBorderingTiles()]
        sp = [i.getType() for i in borderingTiles]
        for i in tilesToChoose:
            while i in sp:
                ind = sp.index(i)
                bestTile = borderingTiles.pop(ind)
                sp.pop(ind)
                if bestTile not in self.getTiles() and\
                        not bestTile.occupied:
                    self.addTile(bestTile)
                    return
