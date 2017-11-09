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
        if destination.x > self.position.x and self.isTileFreeForMonster(self.speed, 0, mapList):
            self.position.x += self.speed
            self.moveCounter = 0
        elif destination.x < self.position.x and self.isTileFreeForMonster(-self.speed, 0, mapList):
            self.position.x -= self.speed
            self.moveCounter = 0
        if destination.y > self.position.y and self.isTileFreeForMonster(0, self.speed, mapList):
            self.position.y += self.speed
            self.moveCounter = 0
        elif destination.y < self.position.y and self.isTileFreeForMonster(0, -self.speed, mapList):
            self.position.y -= self.speed
            self.moveCounter = 0
    def isTileFreeForMonster(self, dX, dY, mapList):
        mapTile = mapList[self.position.y + dY][self.position.x + dX]
        if mapTile.passable and mapTile.char == ',':
            return True
        elif self.isFlying:
            return True
        return False
