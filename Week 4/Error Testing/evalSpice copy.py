import numpy as np
import os




def compListExtractor(stringList,voltageSourceDict, resistorDict, currentSourceDict, nodeSet, rList, vSourceList, iSourceList):
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
                if(splitString[0] not in vSourceList):
                    vSourceList.append(splitString[0])
                else:
                    print(splitString[0], vSourceList)
                    raise ValueError('Malformed circuit file')

                voltageSourceDict[splitString[0]] =  (float(splitString[4]), splitString[3], splitString[1], splitString[2])

            elif splitString[0][0] == 'R':
                if(splitString[0] not in rList):
                    rList.append(splitString[0])
                else:
                    print(splitString[0], rList)
                    raise ValueError('Malformed circuit file')
                
                resistorDict [splitString[0]] = (float(splitString[3]), splitString[1], splitString[2])
            elif splitString[0][0] == 'I':
                if(splitString[0] not in iSourceList):
                    iSourceList.append(splitString[0])
                else:
                    print(splitString[0], vSourceList)
                    raise ValueError('Malformed circuit file')
                
                currentSourceDict[splitString[0]] = (float(splitString[4]), splitString[3], splitString[1], splitString[2])

            else:
                raise ValueError ('Only V, I, R elements are permitted')
            j += 1
    except IndexError:
        raise ValueError ('Malformed circuit file')
    
        
def fillYMatrix(admittanceMatrix, constantMatrix, resistorDict, nodeSet, currentSourceDict, voltageSourceDict):
    for R in resistorDict:
        if(resistorDict[R][2] != 'GND'):
            posTerminalIndex = nodeSet.index(resistorDict[R][2])
        else: posTerminalIndex = -1
        if(resistorDict[R][1] != 'GND'):
            negTerminalIndex = nodeSet.index(resistorDict[R][1])
        else: negTerminalIndex = -1

        if(posTerminalIndex != -1):
            admittanceMatrix[posTerminalIndex][posTerminalIndex] += 1/resistorDict[R][0]
        if(negTerminalIndex != -1):
            admittanceMatrix[negTerminalIndex][negTerminalIndex] += 1/resistorDict[R][0]
        if(negTerminalIndex != -1 and posTerminalIndex != -1):
            admittanceMatrix[posTerminalIndex][negTerminalIndex] -= 1/resistorDict[R][0]
            admittanceMatrix[negTerminalIndex][posTerminalIndex] -= 1/resistorDict[R][0]

    voltageCount = 0
    for V in voltageSourceDict:
        if(voltageSourceDict[V][2] != 'GND'):
            posTerminalIndex = nodeSet.index(voltageSourceDict[V][2])
            admittanceMatrix[len(nodeSet) + voltageCount - 1][posTerminalIndex] += 1
        else: posTerminalIndex = -1
        if(voltageSourceDict[V][3] != 'GND'):
            negTerminalIndex = nodeSet.index(voltageSourceDict[V][3])
            admittanceMatrix[len(nodeSet) + voltageCount - 1][negTerminalIndex] -= 1
        else: negTerminalIndex = -1
        
        if(posTerminalIndex != -1):
            admittanceMatrix[posTerminalIndex][len(nodeSet) + voltageCount - 1] += 1
        if(negTerminalIndex != -1):
            admittanceMatrix[negTerminalIndex][len(nodeSet) + voltageCount - 1] -= 1
        constantMatrix[len(nodeSet) + voltageCount - 1][0] += voltageSourceDict[V][0]
        voltageCount += voltageCount

    for I in currentSourceDict:
        if(currentSourceDict[I][2] != 'GND'):
            constantMatrix[nodeSet.index(currentSourceDict[I][2])][0] -= currentSourceDict[I][0]

        if(currentSourceDict[I][3] != 'GND'):
            constantMatrix[nodeSet.index(currentSourceDict[I][3])][0] += currentSourceDict[I][0]



def createOutputDicts(solutionMatrix, nodeSet, vSourceList, voltageSourceDict):
    outVoltDict = {}
    outCurrDict = {}

    for i in range(len(nodeSet)):
        outVoltDict[nodeSet[i]] = solutionMatrix[i][0]
    outVoltDict['GND'] = 0


    for j in range(len(nodeSet), len(nodeSet) + len(voltageSourceDict)):
        outCurrDict[vSourceList[j - len(nodeSet)]] = solutionMatrix[j][0]

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

    
    voltageSourceDict = {}
    resistorDict = {}
    currentSourceDict = {}

    nodeSet = []
    vSourceList = []
    iSourceList = []
    rList = []

    compListExtractor(stringList, voltageSourceDict, resistorDict, currentSourceDict, nodeSet, rList, vSourceList, iSourceList)
    nodeSet.remove('GND')
    nodeCount = len(nodeSet)
    modifiedAdmittanceMatrix = np.zeros((nodeCount + len(voltageSourceDict), nodeCount + len(voltageSourceDict)))
    constantsMatrix = np.zeros((nodeCount + len(voltageSourceDict), 1))

    fillYMatrix(modifiedAdmittanceMatrix, constantsMatrix, resistorDict, nodeSet, currentSourceDict, voltageSourceDict)
    try:
        solutionMatrix = np.linalg.solve(modifiedAdmittanceMatrix, constantsMatrix)
    except np.linalg.LinAlgError:
        raise ValueError('Circuit error: no solution')
    
    (outputVoltageDict, outputCurrentDict) = createOutputDicts(solutionMatrix, nodeSet, vSourceList, voltageSourceDict)
    
    return (outputVoltageDict, outputCurrentDict)

