class MultiDoor:
    def __init__(self, location, id, levers_needed, char='', isOpen=False): # Mieti
        self.location = location
        if not isOpen:
            self.char = 'D'
            self.passable = False
        else:
            self.char = 'd'
            self.passable = True
        self.id = id
        self.isOpen = isOpen
        self.levers_needed = levers_needed
    def switch(self):
        self.isOpen = not self.isOpen
        if not self.isOpen:
            self.char = 'D'
            self.passable = False
        else:
            self.char = 'd'
            self.passable = True
