from point2d import Point2D

class FlashingWall:
    def __init__(self, location, id, isSolid=False):
        self.location = location
        if not isSolid:
            self.char = '.'
            self.passable = True
        else:
            self.char = '#'
            self.passable = False
        self.id = id
        self.isSolid = isSolid
    def switch(self):
        self.isSolid = not self.isSolid
        if not self.isSolid:
            self.char = '.'
            self.passable = True
        else:
            self.char = '#'
            self.passable = False

