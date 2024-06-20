import csv
import io

def csv_countfruits(msg):
    fruitsDict = {}

    repeatedFruitsDict = csv.DictReader(open(msg), delimiter=',')
    for r in repeatedFruitsDict:
        if(r['Fruit'] not in fruitsDict.keys()):
            fruitsDict[r['Fruit']] = int(r['Number'])
        else:
            fruitsDict[r['Fruit']] += int(r['Number'])
    return fruitsDict

print(csv_countfruits("fruits.csv"))