def matmul (m1, m2):
    if (not hasattr(m1[0], '__iter__') or not hasattr(m2[0], '__iter__')):
        raise TypeError
    
    productMatrix = [[0 for j in range(len(m2))] for i in range(len(m1))]
    for row in range(len(m1)):
        for column in range(len(m2[0])):
            temp = 0
            for current in range(len(m2)):
                temp += m1[row][current] * m2[current][column]
            productMatrix[row][column] = temp

    return productMatrix

print(matmul([[1, 2], [3,4]], [[1, 0],[0, 1]]))