def binsearch(L, v):
    lo = 0
    hi = len(L)-1
   
    while lo <= hi:
        mid = (lo + hi) // 2
        s = L[mid]

        if s == v:
            return mid
        elif s < v:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1

L = [1,2,3,4,5]
print(binsearch(L, 1))