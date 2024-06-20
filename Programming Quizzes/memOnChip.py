import math

def gridpaths(M, N, x1, y1, x2, y2):
    deltaX = abs(x2 - x1)
    deltaY = abs(y2 - y1)
    totalMoves = deltaX + deltaY
    numberOfPaths = math.factorial(totalMoves)//(math.factorial(deltaX) * math.factorial(deltaY))
    
    return numberOfPaths

print(gridpaths(5, 5, 0, 0, 5, 5))
