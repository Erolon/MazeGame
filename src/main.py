from point2d import Point2D
from tile import Tile
from player import Player
from lever import Lever
from door import Door
from mapdataholder import MapDataHolder
from multilever import MultiLever
from multidoor import MultiDoor
from monster import Monster
from mine import Mine
from Libraries.getch import getch
from colorama import init, Fore, Back, Style
import os

message = ""
level_number = 11

def isLevelCompleted(mapList, player):
    if mapList[player.location.y][player.location.x].char == GOAL_CHAR:
        return True
    return False

def main():
    init(autoreset=True)
    play(1)

def isClosedDoorAtPoint(x, y, doors):
    for door in doors:
        if door.location.x == x and door.location.y == y and not door.isOpen:
            return True
    return False

def getItemAtPoint(x, y, items):
    for i in items:
        if i.location.x == x and i.location.y == y:
            return i

def isItemAtPoint(x, y, items):
    for i in items:
        if i.location.x == x and i.location.y == y:
            return True
    return False

def play(current_level, message=""):
    levers = []
    doors = []
    multi_levers = []
    multi_doors = []
    monsters = []
    mines = []
    data_holder = MapDataHolder(levers, doors, multi_levers, multi_doors, monsters, mines)

    if message == "":
        message = "Level " + str(current_level) + "/" + str(level_number)
    else:
        message += "\nLevel " + str(current_level) + "/" + str(level_number)

    if current_level == 1:
        message += " ('h' for help)"

    with open("Maps/" + str(current_level) + ".map") as file:
        mapList = [[tileForChar(char) for char in list(line.rstrip())] for line in file] # Reference [y, x]

    height = len(mapList)
    width = len(mapList[0])

    # Read data
    player = Player(Point2D(0, 0))
    with open("Maps/" + str(current_level) + ".dat") as file:
        lines = [line.rstrip('\n') for line in file]
        for line in lines:
            # Player
            if line.startswith("player"):
                numbers = line.split('=')[1]
                split = numbers.split(',')
                first = split[0]
                second = split[1]
                player.location = Point2D(int(first), int(second))
            elif line.startswith("monster"): # monster.1-2;1:ground=5,3 # id, mf, speed
                numbers = line.split('=')[1]
                split = numbers.split(',')
                x = int(split[0])
                y = int(split[1])
                id = int(line.split('-')[0].split('.')[1])
                moveFrequency = int(line.split(';')[0].split('-')[1])
                speed = int(line.split(':')[0].split(';')[1])
                isFlying = 0
                isFlyingString = line.split('=')[0].split(':')[1]
                if isFlyingString == "fly":
                    isFlying = True
                elif isFlyingString == "ground":
                    isFlying = False
                data_holder.monsters.append(Monster(Point2D(x, y), speed, moveFrequency, isFlying, id, MONSTER_CHAR))
            elif line.startswith("mine"):
                numbers = line.split('=')[1]
                split = numbers.split(',')
                first = int(split[0])
                second = int(split[1])
                data_holder.mines.append(Mine(Point2D(first, second), MINE_CHAR))
            elif line.startswith("lever"): #lever-1=5,5
                values = line.split('=')
                leverNumber = int(values[0].split('-')[1])
                x = int(values[1].split(',')[0])
                y = int(values[1].split(',')[1])
                data_holder.levers.append(Lever(Point2D(x, y), LEVER_CHAR, False, leverNumber)) # The items must be in order in the file
            elif line.startswith("door"): #door-1=6,4
                values = line.split('=')
                doorNumber = int(values[0].split('-')[1])
                x = int(values[1].split(',')[0])
                y = int(values[1].split(',')[1])
                data_holder.doors.append(Door(Point2D(x, y), doorNumber, isOpen=False))
            elif line.startswith("multi_lever"):
                id = int(line.split('-')[0].split('.')[1])
                number = int(line.split('-')[1].split('=')[0])
                x = int(line.split('=')[1].split(',')[0])
                y = int(line.split('=')[1].split(',')[1])
                data_holder.multi_levers.append(MultiLever(Point2D(x, y), LEVER_CHAR, False, id, number)) # temporary
            elif line.startswith("multi_door"): # multi_door.1-1+2+3=4,2
                id = int(line.split('-')[0].split('.')[1])
                x = int(line.split('=')[1].split(',')[0])
                y = int(line.split('=')[1].split(',')[1])
                levers_needed = []
                lever_numbers = line.split('-')[1].split('=')[0]
                temp = 0
                for c in lever_numbers:
                    if c == '+':
                        levers_needed.append(temp)
                        temp = 0
                    else:
                        temp += int(c)
                levers_needed.append(temp)
                data_holder.multi_doors.append(MultiDoor(Point2D(x, y), id, levers_needed, isOpen=False))

    # Game loop
    gameRunning = True
    while (gameRunning):
        os.system("clear")
        print(message)
        drawMap(player, mapList, data_holder)
        print("> ")
        ch = getch()
        if ch == 'q':
            gameRunning = False
            quit()
        elif ch == 'k':
            new_level = current_level - 1
            if new_level < 1:
                continue
            else:
                play(current_level - 1)
        elif ch == 'l': # Skip level
            new_level = current_level + 1
            if new_level > level_number:
                continue
            else:
                play(current_level + 1)
        elif ch == 'h': # help
            help()
        elif ch == 's':
            playerMovement(0, 1, data_holder, player, mapList, current_level)
        elif ch == 'w':
            playerMovement(0, -1, data_holder, player, mapList, current_level)
        elif ch == 'a':
            playerMovement(-1, 0, data_holder, player, mapList, current_level)
        elif ch == 'd':
           playerMovement(1, 0, data_holder, player, mapList, current_level)

        if isLevelCompleted(mapList, player):
            if current_level == level_number:
                end(player, mapList, data_holder)
            else:
                play(current_level + 1)

def playerMovement(dX, dY, data_holder, player, mapList, current_level):
    newX = player.location.x + dX
    newY = player.location.y + dY
    if isItemAtPoint(newX, newY, data_holder.levers):
        lever = getItemAtPoint(newX, newY, data_holder.levers)
        data_holder.doors[lever.id - 1].switch()
    elif isItemAtPoint(newX, newY, data_holder.multi_levers):
        lever = getItemAtPoint(newX, newY, data_holder.multi_levers)
        lever.switch()
        data_holder.multi_doors[lever.id - 1].levers_needed[lever.number - 1] = 0
        levers_needed = data_holder.multi_doors[lever.id - 1].levers_needed
        if all(i is 0 for i in levers_needed):
            data_holder.multi_doors[lever.id - 1].switch()
    elif isItemAtPoint(newX, newY, data_holder.mines) and getItemAtPoint(newX, newY, data_holder.mines).alive:
        play(current_level, "You were killed by a mine!")
    elif (mapList[newY][newX].passable) and not isClosedDoorAtPoint(newX, newY, data_holder.doors) and not isClosedDoorAtPoint(newX, newY, data_holder.multi_doors):
        player.location.x = newX
        player.location.y = newY
    updateMonsters(data_holder, mapList, newX, newY)
    for m in data_holder.monsters:
        if m.position.x == player.location.x and m.position.y == player.location.y and m.alive:
            play(current_level, "You were killed by a monster!")

def updateMonsters(data_holder, mapList, playerX, playerY):
    for m in data_holder.monsters:
        m.move(Point2D(playerX, playerY), mapList, data_holder)

def help():
    os.system("clear")
    print("-- Controls --\n- Use 'wasd' to move\n- Exit the game with 'q'\nExperiment with objects and try to reach the purple goal!")
    getch()

def end(player, mapList, data_holder):
    os.system("clear")
    print("Congratulations! You have completed all " + str(level_number) + " levels.")
    drawMap(player, mapList, data_holder)
    quit()

def drawMap(player, mapList, data_holder):
    height = len(mapList)
    width = len(mapList[0])

    for y in range(height):
        for x in range(width):
            wasOtherPrinted = False
            wasPlayerAtLocation = False
            if y == player.location.y and x == player.location.x:
                print(Fore.YELLOW + Back.WHITE + PLAYER_CHAR, end='')
                wasOtherPrinted = True
                wasPlayerAtLocation = True
            for lever in data_holder.levers:
                if y == lever.location.y and x == lever.location.x:
                    print(Fore.GREEN + Back.WHITE + lever.char, end='')
                    wasOtherPrinted = True
            for door in data_holder.doors:
                if x == door.location.x and y == door.location.y and not wasPlayerAtLocation:
                    print(Fore.BLUE + Back.WHITE + door.char, end='')
                    wasOtherPrinted = True
            for lever in data_holder.multi_levers:
                if y == lever.location.y and x == lever.location.x:
                    print(Fore.GREEN + Back.WHITE + lever.char, end='')
                    wasOtherPrinted = True
            for door in data_holder.multi_doors:
                if x == door.location.x and y == door.location.y and not wasPlayerAtLocation:
                    print(Fore.BLUE + Back.WHITE + door.char, end='')
                    wasOtherPrinted = True
            for m in data_holder.monsters:
                if x == m.position.x and y == m.position.y and m.alive:
                    print(Fore.RED + Back.WHITE + m.char, end='')
                    wasOtherPrinted = True
            for m in data_holder.mines:
                if x == m.location.x and y == m.location.y and m.alive:
                    print(Fore.LIGHTRED_EX + Back.WHITE + m.char, end='')
                    wasOtherPrinted = True

            if not wasOtherPrinted:
                if x == width - 1:
                    print(Fore.RED + Back.RED + mapList[y][x].char) # Always a wall
                else:
                    char = mapList[y][x].char
                    if char == WALL_CHAR:
                        print(Fore.RED + Back.RED + mapList[y][x].char, end='')
                    elif char == EMPTY_CHAR or char == MONSTER_AREA_CHAR:
                        print(Fore.WHITE + Back.WHITE + EMPTY_CHAR, end='')
                    elif char == GOAL_CHAR:
                        print(Fore.MAGENTA + Back.MAGENTA + mapList[y][x].char, end='')
                    else:
                        print(mapList[y][x].char, end='')

WALL_CHAR = '#'
EMPTY_CHAR = '.'
PLAYER_CHAR = '@'
GOAL_CHAR = '0'
LEVER_CHAR = 'L'
DOOR_CLOSED_CHAR = 'D'
DOOR_OPEN_CHAR = 'd'
MONSTER_CHAR = 'M'
MONSTER_AREA_CHAR = ','
MINE_CHAR = 'O'

def tileForChar(char):
    if char == WALL_CHAR:
        return Tile(char, False)
    elif char == EMPTY_CHAR or char == PLAYER_CHAR or char == GOAL_CHAR or char == MONSTER_AREA_CHAR:
        return Tile(char, True)
    elif char == LEVER_CHAR:
        return Tile(WALL_CHAR, False) # Return a wall
    elif char == DOOR_CLOSED_CHAR:
        return Tile(EMPTY_CHAR, True) # Needs to be passable
    elif char == MONSTER_CHAR or char == MINE_CHAR:
        return Tile(MONSTER_AREA_CHAR, True)
    else:
        print("found " + char)

main()
