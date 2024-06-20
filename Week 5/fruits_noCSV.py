import io

msg = """
Fruit,Number
Apple,3
Orange,5
Banana,4
Apple,7
Apple,2
Banana,3
"""
def csv_countfruits(msg):
    fruitsDict = {}
    sfp = io.StringIO(msg).readlines()
    for i in range(2, len(sfp)):
        splitLine = sfp[i].split(sep = ",")
        if(splitLine[0] not in fruitsDict.keys()):
            fruitsDict[splitLine[0]] = int(splitLine[1])
        else:
            fruitsDict[splitLine[0]] += int(splitLine[1])

    return fruitsDict

print(csv_countfruits(msg))