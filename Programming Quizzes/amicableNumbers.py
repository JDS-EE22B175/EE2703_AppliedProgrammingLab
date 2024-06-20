def properDivisors(N):
    properDivisorSum = 1
    for i in range(2, N//2 + 1):
        if(N % i == 0):
            properDivisorSum += i

    return properDivisorSum

def amicable(n1, n2):
    if(n1 == n2):
        return False
    
    pDivSumN1 = properDivisors(n1)
    pDivSumN2 = properDivisors(n2)
    if(pDivSumN1 == n2 and pDivSumN2 == n1):
        return True
    
    return False
    
def amsum(N):
    amicableSum = 0
    divisorSums = [properDivisors(i) for i in range(12, N + 1)]
    #print(divisorSums)
    for i in range(len(divisorSums) - 1):
        if(divisorSums[i] == 1):
            continue
        
        n1 = i + 12
        n2 = divisorSums[i]

        #print(i, n1, n2)
        if ((n2 > n1 and n2 < N + 1) and divisorSums[n2 - 12] == n1):
            amicableSum += n1 + n2

    return amicableSum

print(amsum(20000))