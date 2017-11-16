class Mine:
    def __init__(self, location, char):
        self.location = location
        self.char = char
        self.alive = True
    def kill(self):
        self.alive = False
