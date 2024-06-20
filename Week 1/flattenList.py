def flatten(l):
    fList = []
    for i in range(0, len(l)):
        if(type(l[i]) is list):
            for j in range(0, len(l[i])):
                fList.append(l[i][j])
        else: fList.append(l[i])
    return fList

print(flatten([1, [2,3]]))