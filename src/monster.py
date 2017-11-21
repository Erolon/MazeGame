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
        if destination.x > self.position.x and self.isTileFreeForMonster(self.speed, 0, mapList, data_holder):
            self.position.x += self.speed
            self.moveCounter = 0
        elif destination.x < self.position.x and self.isTileFreeForMonster(-self.speed, 0, mapList, data_holder):
            self.position.x -= self.speed
            self.moveCounter = 0
        if destination.y > self.position.y and self.isTileFreeForMonster(0, self.speed, mapList, data_holder):
            self.position.y += self.speed
            self.moveCounter = 0
        elif destination.y < self.position.y and self.isTileFreeForMonster(0, -self.speed, mapList, data_holder):
            self.position.y -= self.speed
            self.moveCounter = 0
        self.checkForMines(self.position.x, self.position.y, data_holder)
    def isTileFreeForMonster(self, dX, dY, mapList, data_holder):
        newX = self.position.x + dX
        newY = self.position.y + dY
        mapTile = mapList[self.position.y + dY][self.position.x + dX]
        if mapTile.passable and (mapTile.char == ',' or mapTile.char == 'O') and not self.checkForMonster(newX, newY, data_holder.monsters):
            return True
        elif self.isFlying and not self.checkForMonster(newX, newY, data_holder.monsters):
            return True
        return False
    def checkForMines(self, x, y, data_holder):
        for m in data_holder.mines:
            if m.location.x == x and m.location.y == y and m.alive:
                self.alive = False
                m.kill()
    def checkForMonster(self, x, y, items):
        for i in items:
            if i.position.x == x and i.position.y == y:
                return True
        return False
