import numpy as np
import os


voltageSourceList = {}
resistorList = {}
currentSourceList = {}
nodeSet = []
vSourceSet = []
iSourceSet = []
rSet = []
nodeCount = 0

def resetGlobals():
    global voltageSourceList, resistorList, currentSourceList, nodeSet, vSourceSet, iSourceSet, rSet, nodeCount
    voltageSourceList = {}
    resistorList = {}
    currentSourceList = {}
    nodeSet = []
    vSourceSet = []
    iSourceSet = []
    rSet = []
    nodeCount = 0

def compListExtractor(stringList):
    j = 0
    #  Looking for where the circuit definition starts from
    try:
        while (stringList[j] != ".circuit\n" and stringList[j] != ".circuit"):
            j += 1
    except IndexError:
        raise ValueError ('Malformed circuit file')

    j = j + 1

    try:
        while (stringList[j] != ".end\n" and stringList[j] != ".end"):
            splitString = stringList[j].split()

            if(splitString[1] not in nodeSet):
                nodeSet.append(splitString[1])
            if(splitString[2] not in nodeSet):
                nodeSet.append(splitString[2])

            if splitString[0][0] == 'V':
                if(splitString[0] not in vSourceSet):
                    vSourceSet.append(splitString[0])
                else:
                    print(splitString[0], vSourceSet)
                    raise ValueError('Malformed circuit file')

                voltageSourceList[splitString[0]] =  (float(splitString[4]), splitString[3], splitString[1], splitString[2])

            elif splitString[0][0] == 'R':
                if(splitString[0] not in rSet):
                    rSet.append(splitString[0])
                else:
                    print(splitString[0], rSet)
                    raise ValueError('Malformed circuit file')
                
                resistorList [splitString[0]] = (float(splitString[3]), splitString[1], splitString[2])
            elif splitString[0][0] == 'I':
                if(splitString[0] not in iSourceSet):
                    iSourceSet.append(splitString[0])
                else:
                    print(splitString[0], vSourceSet)
                    raise ValueError('Malformed circuit file')
                
                currentSourceList[splitString[0]] = (float(splitString[4]), splitString[3], splitString[1], splitString[2])

            else:
                raise ValueError ('Only V, I, R elements are permitted')
            j += 1
    except IndexError:
        raise ValueError ('Malformed circuit file')
    
        
def fillYMatrix(admittanceMatrix, constantMatrix):
    for R in resistorList:
        if(resistorList[R][2] != 'GND'):
            posTerminalIndex = nodeSet.index(resistorList[R][2])
        else: posTerminalIndex = -1
        if(resistorList[R][1] != 'GND'):
            negTerminalIndex = nodeSet.index(resistorList[R][1])
        else: negTerminalIndex = -1

        if(resistorList[R][0] != 0):
            if(posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][posTerminalIndex] += 1/resistorList[R][0]
            if(negTerminalIndex != -1):
                admittanceMatrix[negTerminalIndex][negTerminalIndex] += 1/resistorList[R][0]
            if(negTerminalIndex != -1 and posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][negTerminalIndex] -= 1/resistorList[R][0]
                admittanceMatrix[negTerminalIndex][posTerminalIndex] -= 1/resistorList[R][0]

        else:
            if(posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][posTerminalIndex] = float('inf')
            if(negTerminalIndex != -1):
                admittanceMatrix[negTerminalIndex][negTerminalIndex] = float('inf')

            if(negTerminalIndex != -1 and posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][negTerminalIndex] = 0
                admittanceMatrix[negTerminalIndex][posTerminalIndex] = 0

    voltageCount = 0
    for V in voltageSourceList:
        if(voltageSourceList[V][2] != 'GND'):
            posTerminalIndex = nodeSet.index(voltageSourceList[V][2])
            admittanceMatrix[nodeCount + voltageCount - 1][posTerminalIndex] += 1
        else: posTerminalIndex = -1
        if(voltageSourceList[V][3] != 'GND'):
            negTerminalIndex = nodeSet.index(voltageSourceList[V][3])
            admittanceMatrix[nodeCount + voltageCount - 1][negTerminalIndex] -= 1
        else: negTerminalIndex = -1
        
        if(posTerminalIndex != -1):
            admittanceMatrix[posTerminalIndex][nodeCount + voltageCount - 1] += 1
        if(negTerminalIndex != -1):
            admittanceMatrix[negTerminalIndex][nodeCount + voltageCount - 1] -= 1
        constantMatrix[nodeCount + voltageCount - 1][0] += voltageSourceList[V][0]
        voltageCount += voltageCount

    for I in currentSourceList:
        if(currentSourceList[I][2] != 'GND'):
            constantMatrix[nodeSet.index(currentSourceList[I][2])][0] -= currentSourceList[I][0]

        if(currentSourceList[I][3] != 'GND'):
            constantMatrix[nodeSet.index(currentSourceList[I][3])][0] += currentSourceList[I][0]



def createOutputDicts(solutionMatrix):
    outVoltDict = {}
    outCurrDict = {}

    for i in range(len(nodeSet)):
        outVoltDict[nodeSet[i]] = solutionMatrix[i][0]
    outVoltDict['GND'] = 0


    for j in range(len(nodeSet), len(nodeSet) + len(voltageSourceList)):
        outCurrDict[vSourceSet[j - len(nodeSet)]] = solutionMatrix[j][0]

    return (outVoltDict, outCurrDict)

def evalSpice(filename):
    fileSplit = os.path.splitext(filename)
    if(fileSplit[-1] != ".ckt"):
        raise FileNotFoundError ('Please give the name of a valid SPICE file as input')

    fPointer = open(filename, "r")

    if(fPointer == None):
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')

    stringList = fPointer.readlines()
    fPointer.close()

    resetGlobals()

    compListExtractor(stringList)
    nodeSet.remove('GND')
    nodeCount = len(nodeSet)
    modifiedAdmittanceMatrix = np.zeros((nodeCount + len(voltageSourceList), nodeCount + len(voltageSourceList)))
    constantsMatrix = np.zeros((nodeCount + len(voltageSourceList), 1))

    fillYMatrix(modifiedAdmittanceMatrix, constantsMatrix)
    try:
        solutionMatrix = np.linalg.solve(modifiedAdmittanceMatrix, constantsMatrix)
    except np.linalg.LinAlgError:
        raise ValueError('Circuit error: no solution')
    
    (outputVoltageDict, outputCurrentDict) = createOutputDicts(solutionMatrix)

    return (outputVoltageDict, outputCurrentDict)

print(evalSpice("test_0_R.ckt"))