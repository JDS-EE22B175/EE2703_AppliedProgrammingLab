def gausselim(A, B):
    # Normalize row 1
    norm = A[0][0]
    for i in range(len(A[0])): A[0][i] /= norm
    B[0] = B[0]/norm

    # Eliminate row 2 - A[1] 
    for k in range(len(A[0]) - 1):
        for j in range(k+1, len(A)):
            norm = A[j][k] / A[k][k]
            for i in range(k, len(A[j])): A[j][i] = A[j][i] - A[k][i] * norm
            B[j] = B[j] - B[k] * norm

    # Normalize row 2 - B[1] will now contain the solution for x2
    for j in range(len(A)):
        norm = A[j][j]
        for i in range(len(A[j])): A[j][i] = A[j][i] / norm
        B[j] = B[j] / norm

    # Sub back and solve for B[0] <-> x1
    # This can be seen as eliminating A[0][1]
    for k in range(len(A) - 1, 0, -1):
        for j in range(k):
            norm = A[j][k]
        # note that len(A) will give number of rows
            for i in range(len(A[0])): 
                A[j][i] = A[j][i] - A[k][i] * norm
            B[j] = B[j] - B[k]* norm    

    return B


A = [ [7,1, 5], [4,3, 5], [6, 1, 2] ]
B = [27, 21, 9]


A4 = [[1, 0, 1, 2], [0, 1, -2, 0],[1, 2, -1, 0], [2, 1, 3, -2]]
B4 = [6, -3, -2, 0]
print(gausselim(A4, B4))
