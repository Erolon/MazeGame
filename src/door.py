from point2d import Point2D

class Door:
    def __init__(self, location, id, char='', isOpen=False):
        self.location = location
        if not isOpen:
            self.char = 'D'
            self.passable = False
        else:
            self.char = 'd'
            self.passable = True
        self.id = id
        self.isOpen = isOpen
    def switch(self):
        self.isOpen = not self.isOpen
        if not self.isOpen:
            self.char = 'D'
            self.passable = False
        else:
            self.char = 'd'
            self.passable = True
