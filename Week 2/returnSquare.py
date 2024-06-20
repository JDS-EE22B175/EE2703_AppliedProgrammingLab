def list_compre_div(l, N):
    returnList = []
    for i in l:
        if (i%N == 0):
            returnList.append(i**2)
    return returnList

print(list_compre_div([1,2,3,4,5,6,7,8], 2))