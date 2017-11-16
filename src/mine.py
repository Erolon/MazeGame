class Mine:
    def __init__(self, isPlaced, location, char):
        self.isPlaced = isPlaced
        self.location = location
        self.char = char
        self.alive = True
    def kill(self):
        self.alive = False
