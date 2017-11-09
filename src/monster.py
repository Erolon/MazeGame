class Monster:
    def __init__(self, position, speed, moveFrequency, id, char):
        self.position = position
        self.speed = speed
        self.id = id
        self.char = char
        self.moveCounter = 0
        self.moveFrequency = moveFrequency - 1
    def move(self, destination):
        if not self.moveFrequency == self.moveCounter:
            self.moveCounter += 1
            return
        if destination.x > self.position.x:
            self.position.x += self.speed
        elif destination.x < self.position.x:
            self.position.x -= self.speed
        if destination.y > self.position.y:
            self.position.y += self.speed
        elif destination.y < self.position.y:
            self.position.y -= self.speed
        self.moveCounter = 0