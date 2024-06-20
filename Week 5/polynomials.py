import math

def polyadd(A, B):
    if (len(A) >= len(B)):
        lowerOrder = len(B)
        largerPoly = A
        smallerPoly = B
    else:
        lowerOrder = len(A)
        largerPoly = B
        smallerPoly = A
        
    for i in range(lowerOrder):
        largerPoly[i] += smallerPoly[i]
    
    return largerPoly
    
def polymul(A, B):
    prodPoly = [0 for e in range(len(A) + len(B) - 1)]
    for j in range(len(A)):
        for i in range(len(B)):
            prodPoly[i+j] += A[j] * B[i]
    
    return prodPoly

def polydiv(A, B):
    Q = []
    stepCounter = 0
    for i in range(len(A) - 1, len(B) - 2, -1):
        Q.insert(0, A[i]/B[-1])
        subractor = [j * (-A[i]/B[-1]) for j in B]
        for j in range(len(B), len(A) - stepCounter):
            subractor.insert(0, 0)
        A = polyadd(A, subractor)
        stepCounter += 1
    R = []
    for r in range(len(B) - 1):
        R.append(A[r])
        
    return (Q, R)
    
def pr_help(l):
    return ",".join(map(str, map(float, l)))

print(polydiv([7, 3, 5], [10, 2]))