import math

def drawLine(highPoint, lowPoint, x):
    f = lowPoint[1] + ((highPoint[1] - lowPoint[1])/(highPoint[0] - lowPoint[0])) * (x - lowPoint[0])
    return f

def interp(x, xp, fp):

    fVals = []
    for xVal in x:
        lowerX = xp[0]
        higherX = xp[-1]

        if (xVal <= xp[0]):
            fVals.append(fp[0])
            continue

        elif (xVal >= xp[-1]):
            fVals.append(fp[-1])
            continue

        for givenX in xp:
            if(xVal - givenX > 0 and math.fabs(xVal - givenX) < math.fabs(xVal - lowerX)):
                lowerX = givenX
            if(xVal - givenX < 0 and math.fabs(xVal - givenX) < math.fabs(xVal - higherX)):
                higherX = givenX
            
        fVals.append(drawLine([higherX, fp[xp.index(higherX)]], [lowerX, fp[xp.index(lowerX)]], xVal))

    return fVals

xp=[10, 12, 14, 16, 18]
fp=[100, 144, 196, 256, 324]
x=[ 5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
print(interp(x, xp, fp))