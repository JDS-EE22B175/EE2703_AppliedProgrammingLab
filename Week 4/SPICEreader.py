import io
def circuit_count(msg):
    sfp = io.StringIO(msg)
    stringList =  sfp.readlines()
    j = 1
    while stringList[j] != ".circuit\n":
        j += 1

    j = j + 1
    componentDict = {}
    while stringList[j] != ".end\n":
        for i in stringList[j]:
            if(i != "\n"):
                if(i not in componentDict.keys()):
                    componentDict[i] = 1
                    break
                else:
                    componentDict[i] += 1
                    break
        j += 1

    return componentDict

msg = """
This is a test circuit with some junk in front.

.circuit

Vsource n1 GND 10

Isource n3 GND 1

R1 n1 n2 2

R2 n2 n3 5

L3 n2 GND 3

.end
"""
print(circuit_count(msg))