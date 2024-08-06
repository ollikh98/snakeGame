import random
from bidict import bidict
def screenToGameCoord(map, pos):
    x, y = pos
    gameX = [map[screenPos] for screenPos in map if x in screenPos][0]
    gameY = [map[screenPos] for screenPos in map if y in screenPos][0]

    return (gameX, gameY)


def gameToScreenCord(map,pos):
    x, y = pos

    screenX = map.inverse[x]
    screenY = map.inverse[y]
    screenX = screenX[0]
    screenY = screenY[0]

    return (screenX, screenY)

def generateRandomGamePos(map):
    mapsize = len(map)-1
    newX = random.randint(0,mapsize)
    newY = random.randint(0, mapsize)
    return (newX,newY)


def calctileSize(resolution,mapsize):
    width, height = mapsize
    tileWidth = (resolution[0] / width)
    tileHeight = (resolution[1] / height)

    return (int(tileWidth), int(tileHeight))


def makeMap(resolution, blocksize):
    # uses bidict to have a key<->key pairing for screen to game coordinates
    gridPos = 0
    mapDict = {}

    for x in range(0, resolution[0], blocksize):
        mapDict[range(x, x + blocksize)] = gridPos
        gridPos += 1

    return bidict(mapDict)