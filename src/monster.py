class Monster:
    def __init__(self, position, speed, moveFrequency, isFlying, id, char):
        self.position = position
        self.speed = speed
        self.id = id
        self.char = char
        self.isFlying = isFlying
        self.moveCounter = 0
        self.moveFrequency = moveFrequency - 1
    def move(self, destination, mapList):
        if not self.moveFrequency == self.moveCounter:
            self.moveCounter += 1
            return
        if destination.x > self.position.x and (mapList[self.position.y][self.position.x + self.speed].passable or self.isFlying):
            self.position.x += self.speed
        elif destination.x < self.position.x and (mapList[self.position.y][self.position.x - self.speed].passable or self.isFlying):
            self.position.x -= self.speed
        if destination.y > self.position.y and (mapList[self.position.y + self.speed][self.position.x].passable or self.isFlying):
            self.position.y += self.speed
        elif destination.y < self.position.y and (mapList[self.position.y - self.speed][self.position.x].passable or self.isFlying):
            self.position.y -= self.speed
        self.moveCounter = 0