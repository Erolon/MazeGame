class Mine:
    def __init__(self, isPlaced, position, char):
        self.isPlaced = isPlaced
        self.position = position
        self.char = char
        self.alive = True
    def kill(self):
        self.alive = False
