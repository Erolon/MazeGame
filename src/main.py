from point2d import Point2D
from tile import Tile
from player import Player
from lever import Lever
from door import Door
from mapdataholder import MapDataHolder
from multilever import MultiLever
from multidoor import MultiDoor
from Libraries.getch import getch
from colorama import init, Fore, Back, Style
import os

message = ""
level_number = 7

def isLevelCompleted(mapList, player):
    if mapList[player.location.y][player.location.x].char == GOAL_CHAR:
        return True
    return False

def main():
    init(autoreset=True)
    play(1)

def isLeverAtPoint(x, y, levers):
    for lever in levers:
        if lever.location.x == x and lever.location.y == y:
            return True
    return False

def isClosedDoorAtPoint(x, y, doors):
    for door in doors:
        if door.location.x == x and door.location.y == y and not door.isOpen:
            return True
    return False

def getLeverAtPoint(x, y, levers):
    for lever in levers:
        if lever.location.x == x and lever.location.y == y:
            return lever

def play(current_level):
    levers = []
    doors = []
    multi_levers = []
    multi_doors = []
    data_holder = MapDataHolder(levers, doors, multi_levers, multi_doors)

    message = "Level " + str(current_level) + "/" + str(level_number)
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
            elif line.startswith("multi_door"):
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
            playerMovement(0, 1, data_holder, player, mapList)
        elif ch == 'w':
            playerMovement(0, -1, data_holder, player, mapList)
        elif ch == 'a':
            playerMovement(-1, 0, data_holder, player, mapList)
        elif ch == 'd':
           playerMovement(1, 0, data_holder, player, mapList)

        if isLevelCompleted(mapList, player):
            if current_level == level_number:
                end(player, mapList, data_holder)
            else:
                play(current_level + 1)

def playerMovement(dX, dY, data_holder, player, mapList):
    newX = player.location.x + dX
    newY = player.location.y + dY
    if isLeverAtPoint(newX, newY, data_holder.levers):
        lever = getLeverAtPoint(newX, newY, data_holder.levers)
        data_holder.doors[lever.id - 1].switch()
    elif isLeverAtPoint(newX, newY, data_holder.multi_levers):
        lever = getLeverAtPoint(newX, newY, data_holder.multi_levers)
        lever.switch()
        data_holder.multi_doors[lever.id - 1].levers_needed[lever.number - 1] = 0
        levers_needed = data_holder.multi_doors[lever.id - 1].levers_needed
        if all(i is 0 for i in levers_needed):
            data_holder.multi_doors[lever.id - 1].switch()
    elif (mapList[newY][newX].passable) and not isClosedDoorAtPoint(newX, newY, data_holder.doors):
        player.location.x = newX
        player.location.y = newY

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


            if not wasOtherPrinted:
                if x == width - 1:
                    print(Fore.RED + Back.RED + mapList[y][x].char + Fore.RESET + Back.RESET) # Always a wall
                else:
                    char = mapList[y][x].char
                    if char == '#': # CHANGE TO USE CONSTANTS
                        print(Fore.RED + Back.RED + mapList[y][x].char, end='')
                    elif char == '.':
                        print(Fore.WHITE + Back.WHITE + mapList[y][x].char, end='')
                    elif char == '0':
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

def tileForChar(char):
    if char == WALL_CHAR:
        return Tile(char, False)
    elif char == EMPTY_CHAR or char == PLAYER_CHAR or char == GOAL_CHAR:
        return Tile(char, True)
    elif char == LEVER_CHAR:
        return Tile(WALL_CHAR, False) # Return a wall
    elif char == DOOR_CLOSED_CHAR:
        return Tile(EMPTY_CHAR, True) # Needs to be passable
    else:
        print("found " + char)

main()
