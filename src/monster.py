class Monster:
    def __init__(self, position, speed, id, char):
        self.position = position
        self.speed = speed
        self.id = id
        self.char = char
    def move(self, destination):
        if destination.x > self.position.x:
            self.position.x += self.speed
        elif destination.x < self.position.x:
            self.position.x -= self.speed
        if destination.y > self.position.y:
            self.position.y += self.speed
        elif destination.y < self.position.y:
            self.position.y -= self.speed
