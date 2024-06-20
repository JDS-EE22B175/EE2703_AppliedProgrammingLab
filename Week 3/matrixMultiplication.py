def matmul (m1, m2):
    if (not isinstance(m1[0], list) or not isinstance(m2[0], list)):
        raise TypeError
    
    productMatrix = [[0] * len(m2[0])] * len(m1)
    '''
    for row in range(len(m1)):
        for column in range(len(m2[0])):
            temp = 0
            for current in range(len(m2)):
                temp += m1[row][current] * m2[current][column]
            productMatrix[row][column] = temp
            print(productMatrix[row][column], row, column)
    '''
    print ([id(x) for x in productMatrix])
    return productMatrix

print(matmul([[1,2], [3,4]], [[1, 0],[0, 1]]))