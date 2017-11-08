class MultiLever:
    def __init__(self, location, char, passable, id, number):
        self.location = location
        self.char = char
        self.passable = passable
        self.id = id
        self.number = number
    def switch(self):
        if self.char == 'L':
            self.char = 'l'
        else:
            self.char = 'L'