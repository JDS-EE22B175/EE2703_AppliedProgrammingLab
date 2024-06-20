def gausselim(A, B):
    n = len(A)

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
        
        print(A)


    # Normalize row 2 - B[1] will now contain the solution for x2
    for j in range(len(A)):
        norm = A[j][j]
        for i in range(len(A[j])): A[j][i] = A[j][i] / norm
        B[j] = B[j] / norm

    print(B)
  # Loop over all rows.
    for i in range(n):
        # Find the pivot row, i.e. the row with the largest entry in the current column.
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j

        # Swap the rows i and max_row.
        A[i], A[max_row] = A[max_row], A[i]
        B[i], B[max_row] = B[max_row], B[i]

        # Subtract a multiple of row i from all rows below row i, so that the leading entry of row i becomes 1.
        for j in range(i + 1, n):
            k = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= k * A[i][k]
            B[j] -= k * B[i]

        print(B)
    # Back-solve to find x.
    x = [0] * n
    x[n - 1] = B[n - 1] / A[n - 1][n - 1]

    for i in range(n - 2, -1, -1):
        x[i] = (B[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]

    return x


A = [ [2,3, 4], [1,-1, 2], [1, 5, 3] ]
B = [6, 0.5, 2]

A4 = [[1, 0, 1, 2], [0, 1, -2, 0],[1, 2, -1, 0], [2, 1, 3, -2]]
B4 = [6, -3, -2, 0]
print(gausselim(A4, B4))
