def matmul(m1, m2):
    #  Checking whether the matrices m1 and m2 are nested iterables
    for i in range(len(m1)):
        if (not hasattr(m1[i], '__iter__')):
            raise TypeError  #  If not raising a Type Error
        
    for i in range(len(m2)):
        if (not hasattr(m1[2], '__iter__')):
            raise TypeError  #  If not raising a Type Error
        
    
    #  Checking for Axis Length Mismatch
    if(len(m1[0]) != len(m2)): 
        raise ValueError  #  If so raising a Value Error
    
    #  Creating an empty matrix(nested list with elements zero) with the number of rows of matrix m1 and the number of columns of matrix m2
    productMatrix = [[0 for j in range(len(m2))] for i in range(len(m1))]

    #  Iterating over every row in matrix m1
    for row in range(len(m1)):
        #  Iterating over every column in matrix m2
        for column in range(len(m2[0])):
            #  Iterating over every element in each row of m1 and element of m2, which have the same number of elements
            for current in range(len(m2)):
                #  Multiplying each element in a given row of m1(row) with the corresponding elements in a given column(column) of m2 
                #  and incrementing the element in the given row and column (in the 'row'th row and the 'column'th column)of the product matrix by the product calculated
                productMatrix[row][column] += m1[row][current] * m2[current][column]
                
    #  Returning the product matrix
    return productMatrix

