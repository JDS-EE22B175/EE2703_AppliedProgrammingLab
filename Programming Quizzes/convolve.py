def convolve(A, B):
    aLen = len(A)
    bLen = len(B)
    convolveLen = aLen + bLen - 1
    C = [0 for _ in range(convolveLen)]

    for i in range(convolveLen):
        for j in range(max(0, i - bLen + 1), min(aLen, i + 1)):
            C[i] += A[j] * B[i - j]

    return C


A = [3, 2, 5, 6]
B = [1, 2, 4]
print(convolve(A, B))