def list_rotate(l, N):
    listLength = len(l)
    newList = [None] * listLength
    for i in range(listLength):
        newList[(i+N)%listLength] = l[i]
    return newList

print(list_rotate([1,2,3], 8))