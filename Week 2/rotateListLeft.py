def list_rotate(l, N):
    listLength = len(l)
    N = N % listLength
    newList = [None] * listLength
    for i in range(listLength):
        newList[(i-N)] = l[i]
    return newList

print(list_rotate([1, 2, 3, 4], 1))