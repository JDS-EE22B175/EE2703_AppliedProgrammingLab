def median(l):
    l.sort()
    lLength = len(l)
    if(lLength % 2 == 1):
        return l[lLength//2]
    else:
        return (l[lLength//2] + l[(lLength - 2)//2])/2
    

m=median([1,2,3,4,5,6])
print(m)