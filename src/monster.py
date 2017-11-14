class Monster:
    def __init__(self, position, speed, moveFrequency, isFlying, id, char):
        self.position = position
        self.speed = speed
        self.id = id
        self.char = char
        self.isFlying = isFlying
        self.moveCounter = 0
        self.moveFrequency = moveFrequency - 1
        self.alive = True
    def move(self, destination, mapList, data_holder):
        if not self.alive:
            return
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
        self.checkForMines(self.position.x, self.position.y, data_holder)
    def isTileFreeForMonster(self, dX, dY, mapList):
        mapTile = mapList[self.position.y + dY][self.position.x + dX]
        if mapTile.passable and mapTile.char == ',' or mapTile.char == 'O':
            return True
        elif self.isFlying:
            return True
        return False
    def checkForMines(self, x, y, data_holder):
        for m in data_holder.mines:
            if m.position.x == x and m.position.y == y:
                self.alive = False
