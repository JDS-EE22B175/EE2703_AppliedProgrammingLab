import io
def countfruits(msg):
    stringList = []
    sfp = io.StringIO(msg)
    stringList =  sfp.readlines()
    fruitNames = ["" for i in range(len(stringList))]
    countDict = {}
    for j in range(len(stringList)):
        for i in stringList[j]:
            if(i.isspace() == False and i.isnumeric() == False):
                fruitNames[j] += i
            if(i.isnumeric()):
                if(fruitNames[j] not in countDict.keys()):
                    countDict[fruitNames[j]] = int(i)
                else: countDict[fruitNames[j]] += int(i)
    return countDict

givenString = """
Apple 3
Orange 5
Banana 4
Apple 7
Apple 2
Banana 3
"""

print(countfruits(givenString))
