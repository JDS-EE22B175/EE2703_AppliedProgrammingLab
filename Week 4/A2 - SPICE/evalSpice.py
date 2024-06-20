# Some parts of the matrix creation were made after discussing with Saran Prithive, EE22B165

import numpy as np
import os

# Declaring all of the necessary global variables to limit the number of arguments being passed into each function
voltageSourceList = {}    # Dictionary to store voltage sources
resistorList = {}         # Dictionary to store resistors
currentSourceList = {}    # Dictionary to store current sources
nodeSet = []              # List to store unique circuit nodes
vSourceList = []           # List to store unique voltage sources
iSourceList = []           # List to store unique current sources
rList = []                 # List to store unique resistors
nodeCount = 0

# Function to reset all of the global variables
def resetGlobals():
    global voltageSourceList, resistorList, currentSourceList, nodeSet, vSourceList, iSourceList, rList, nodeCount
    voltageSourceList = {}
    resistorList = {}
    currentSourceList = {}
    nodeSet = []
    vSourceList = []
    iSourceList = []
    rList = []
    nodeCount = 0

# Function to extract components from a list of strings representing a SPICE circuit
def compListExtractor(stringList):
    j = 0
    # Looking for where the circuit definition starts from
    try:
        while (stringList[j] != ".circuit\n" and stringList[j] != ".circuit"):
            j += 1
    # If the start is not encountered, a ValueError is raised with proper feedback
    except IndexError:
        raise ValueError ('Malformed circuit file')

    j = j + 1

    # Looking for the end of the circuit definition
    try:
        while (stringList[j] != ".end\n" and stringList[j] != ".end"):
            # Splitting each line into the name, node1, node2, and value
            splitStringComplete = stringList[j].split()
            splitString = []

            # If the line has more elements than usual
            if((splitStringComplete[0][0] == 'V' or splitStringComplete[0][0] == 'I') and (len(splitStringComplete) > 5)):
                # Checking for comments
                if(splitStringComplete[5][0] == "#"):
                    for i in range(5):
                        splitString.append(splitStringComplete[i])
                # Raising a ValueError if not a comment
                else:
                    raise ValueError ('Malformed circuit file')

            # If the line has more elements than usual
            elif((splitStringComplete[0][0] == 'R') and (len(splitStringComplete) > 5)):
                # Checking for comments
                if(splitStringComplete[4][0] == "#"):
                    for i in range(4):
                        splitString.append(splitStringComplete[i])
                # Raising a ValueError if not a comment
                else:
                    raise ValueError ('Malformed circuit file')
            else:
                splitString = splitStringComplete

            # Adding the nodes that the component is connected to the list of nodes
            if(splitString[1] not in nodeSet):
                nodeSet.append(splitString[1])
            if(splitString[2] not in nodeSet):
                nodeSet.append(splitString[2])

            # If the component is a Voltage Source
            if splitString[0][0] == 'V':
                # Checking if 5 fields are present in the component definition
                if(len(splitString) < 5):
                    raise ValueError('Malformed circuit file') # Raising a ValueError if not
                
                # Checking if this is a new component
                if(splitString[0] not in vSourceList):
                    # If so adding it to a list of voltages sources
                    vSourceList.append(splitString[0]) 
                else:
                    # Raising a ValueError if not
                    raise ValueError('Malformed circuit file')
                
                # Checking if the Source is DC or not
                if(splitString[3] != 'dc'):
                    # Raising a ValueError if not
                    raise ValueError("Only circuits with DC sources can be solved")

                # Storing voltage source information in the dictionary in the format
                # Key = Source Name, Value = (Source Value, ac/dc, Positive Node, Negative Node)
                try:
                    voltageSourceList[splitString[0]] =  (float(splitString[4]), splitString[3], splitString[1], splitString[2])
                except TypeError:
                    raise ValueError('Malformed circuit file')

            # If the component is a Resistor
            elif splitString[0][0] == 'R':
                # Checking if 4 fields are present in the component definition
                if(len(splitString) < 4):
                    raise ValueError('Malformed circuit file') # Raising a ValueError if not
                
                # Checking if this is a new component
                if(splitString[0] not in rList):
                    # If so adding it to a list of resistors
                    rList.append(splitString[0])
                else:
                    # Raising a ValueError if not
                    raise ValueError('Malformed circuit file')
                
                if(float(splitString[3]) < 0):
                    raise ValueError("Resistances Must be Non-negative")
                
                # Storing resistor information in the dictionary in the format
                # Key = Source Name, Value = (Source Value, Positive Node, Negative Node)
                try:
                    resistorList [splitString[0]] = (float(splitString[3]), splitString[1], splitString[2])
                except TypeError:
                    raise ValueError('Malformed circuit file')
            
            # If the component is a Current Source
            elif splitString[0][0] == 'I':
                # Checking if 5 fields are present in the component definition
                if(len(splitString) < 5):
                    raise ValueError('Malformed circuit file') # Raising a ValueError if not
                
                # Checking if this is a new component
                if(splitString[0] not in iSourceList):
                    # If so adding it to a list of current sources
                    iSourceList.append(splitString[0])
                else:
                    # Raising a ValueError if not
                    raise ValueError('Malformed circuit file')
                
                # Checking if the Source is DC or not
                if(splitString[3] != 'dc'):
                    # Raising a ValueError if not
                    raise ValueError("Only circuits with DC sources can be solved")
                
                # Storing current source information in the dictionary in the format
                # Key = Source Name, Value = (Source Value,  ac/dc, Positive Node, Negative Node)
                try:
                    currentSourceList[splitString[0]] = (float(splitString[4]), splitString[3], splitString[1], splitString[2])
                except TypeError:
                    raise ValueError('Malformed circuit file')

            # If the component is not a V, I or R a ValueError is raised with proper feedback
            else:
                raise ValueError ('Only V, I, R elements are permitted')
            
            j += 1
    # If the end is not encountered, a ValueError is raised with proper feedback
    except IndexError:
        raise ValueError ('Malformed circuit file')
    
    try:
        # Removing the Ground node from the nodeSet because the value of the voltage at 'GND' is already assumed to be 0V
        nodeSet.remove('GND')
    # If unable to remove 'GND' from the nodeSet list
    except ValueError:
        # That implies 'GND' node is not in the ckt definition and a ValueError with proper feedback is raised
        raise ValueError("The Circuit MUST contain a 'GND' Node")
    

# Function to fill the Modified Admittance matrix and constants matrix
def fillMatrices(admittanceMatrix, constantMatrix):
    for R in resistorList:
        # Checking if any of the nodes the component is connected to is the Ground node
        # If not the index of the node in the nodeSet is found
        if(resistorList[R][2] != 'GND'):
            posTerminalIndex = nodeSet.index(resistorList[R][2])
        else: posTerminalIndex = -1 # If the node is Ground it is assigned a value of -1
        if(resistorList[R][1] != 'GND'):
            negTerminalIndex = nodeSet.index(resistorList[R][1])
        else: negTerminalIndex = -1 # If the node is Ground it is assigned a value of -1

        # Checking if the resistance is positive
        if(resistorList[R][0] > 0):
        # Based on the positive and negative nodes the resistor is connected to the Modified Admittance matrix is filled
            if(posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][posTerminalIndex] += 1/resistorList[R][0]
            if(negTerminalIndex != -1):
                admittanceMatrix[negTerminalIndex][negTerminalIndex] += 1/resistorList[R][0]
            if(negTerminalIndex != -1 and posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][negTerminalIndex] -= 1/resistorList[R][0]
                admittanceMatrix[negTerminalIndex][posTerminalIndex] -= 1/resistorList[R][0]
        # If it is 0, it is treated as a short circuit
        else:
            # 1/0s are replaced by infinite admittances and 0s as
            if(posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][posTerminalIndex] = float('inf')
            if(negTerminalIndex != -1):
                admittanceMatrix[negTerminalIndex][negTerminalIndex] = float('inf')

            if(negTerminalIndex != -1 and posTerminalIndex != -1):
                admittanceMatrix[posTerminalIndex][negTerminalIndex] = 0
                admittanceMatrix[negTerminalIndex][posTerminalIndex] = 0
        

    voltageCount = 0  # Counter for the for loop to properly fill the admittance matrix
    for V in voltageSourceList:
        # Checking if any of the nodes the component is connected to is the Ground node
        # If not the index of the node in the nodeSet is found
        # The Modified Admittance matrix is filled accordingly
        if(voltageSourceList[V][2] != 'GND'):
            posTerminalIndex = nodeSet.index(voltageSourceList[V][2]) # Setting the +ve terminal index if it is not 'GND'
            admittanceMatrix[nodeCount + voltageCount - 1][posTerminalIndex] += 1
        else: posTerminalIndex = -1 # Setting the +ve terminal index to -1 if it is 'GND'
        if(voltageSourceList[V][3] != 'GND'):
            negTerminalIndex = nodeSet.index(voltageSourceList[V][3]) # Setting the -ve terminal index if it is not 'GND'
            admittanceMatrix[nodeCount + voltageCount - 1][negTerminalIndex] -= 1
        else: negTerminalIndex = -1 # Setting the -ve terminal index to -1 if it is 'GND'
        
        if(posTerminalIndex != -1):
            admittanceMatrix[posTerminalIndex][nodeCount + voltageCount - 1] += 1
        if(negTerminalIndex != -1):
            admittanceMatrix[negTerminalIndex][nodeCount + voltageCount - 1] -= 1
        constantMatrix[nodeCount + voltageCount - 1][0] += voltageSourceList[V][0]
        voltageCount += voltageCount

    for I in currentSourceList:
        # Checking if any of the nodes the component is connected to is the Ground node
        # Based on the positive and negative nodes the current source is connected to the constants matrix is filled
        if(currentSourceList[I][2] != 'GND'):
            constantMatrix[nodeSet.index(currentSourceList[I][2])][0] -= currentSourceList[I][0]

        if(currentSourceList[I][3] != 'GND'):
            constantMatrix[nodeSet.index(currentSourceList[I][3])][0] += currentSourceList[I][0]


# Function to create output dictionaries containing voltage and current values
def createOutputDicts(solutionMatrix):
    outVoltDict = {}
    outCurrDict = {}

    # Filling the Output Voltage Dictionary with all of the 
    # calculated Node Voltages as values and the Node names as the keys
    for i in range(len(nodeSet)):
        outVoltDict[nodeSet[i]] = solutionMatrix[i][0]

    # Adding in the voltage at the Ground Node to the dictionary
    outVoltDict['GND'] = 0

    # Filling the Output Current Dictionary with all of the 
    # calculated Currents through the Voltage Sources as values anf the Source names as the keys
    for j in range(len(nodeSet), len(nodeSet) + len(voltageSourceList)):
        outCurrDict[vSourceList[j - len(nodeSet)]] = solutionMatrix[j][0]

    # Returning the Output Voltage Dictionary and theOutput Current Dictionary
    return (outVoltDict, outCurrDict)


# Function to read in the file and raise file related errors
def readFile(filename):
    fileSplit = os.path.splitext(filename)
    # Finding the file's extension and checking if it is .ckt
    if(fileSplit[-1] != ".ckt"):
        # If not a FileNotFoundError is raised with proper feedback
        raise FileNotFoundError ('Please give the name of a valid SPICE file as input')
    
    # The file is opened in read mode
    fPointer = open(filename, "r")

    # If the file is None was not found a FileNotFoundError is raised with proper feedback
    if(fPointer == None):
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')

    # Each line of the file is stored in a list
    stringList = fPointer.readlines()
    # The file is closed
    fPointer.close()

    return stringList


# Function to evaluate a SPICE circuit given a netlist file 
def evalSpice(filename):
    # Callling the Read File function to get the list of lines in the file
    stringList = readFile(filename)
    # Resetting the global variables before performing the algorithm to keep each run independent of the other
    resetGlobals()
    
    # Calling the Component List Extractor Function giving the list of lines in the file as the argument
    compListExtractor(stringList)

    # Storing the number of nodes in the nodeSet other than the 'GND' node
    nodeCount = len(nodeSet)

    # Creating a zero valued square numpy matrix of the order (number of nodes - 'GND' + number of voltage sources) 
    modifiedAdmittanceMatrix = np.zeros((nodeCount + len(voltageSourceList), nodeCount + len(voltageSourceList)))
    # Creating a zero valued Column numpy matrix of the order (number of nodes - 'GND' + number of voltage sources) x 1
    constantsMatrix = np.zeros((nodeCount + len(voltageSourceList), 1))

    # Calling the Fill Matrices function that fills the Modified Admittance matrix and the constants matrix according to 
    # Modified Nodal Analysis
    fillMatrices(modifiedAdmittanceMatrix, constantsMatrix)

    print(modifiedAdmittanceMatrix, constantsMatrix)

    # Solving for the Node Voltages and the Currents through Voltage Sources
    try:
        solutionMatrix = np.linalg.solve(modifiedAdmittanceMatrix, constantsMatrix)
    # If LinAlg raises an error, that means that the Modified Admittance Matrix is Singular and the circuit cannot be solved
    except np.linalg.LinAlgError:
        # A ValueError is raised
        raise ValueError('Circuit error: no solution')
        # This handles cases like when Voltage Sources in Parallel and Current Sources in Series among others
    
    # The Solution is made into the expected format
    (outputVoltageDict, outputCurrentDict) = createOutputDicts(solutionMatrix)

    # The Output Dictionaries are returned
    return (outputVoltageDict, outputCurrentDict)
print(evalSpice("./testdata/test_4.ckt"))