def dedup(l):
    deDupl = []
    
    for number in l:
        if(number not in deDupl):
            deDupl.append(number)

    return deDupl

l = [4, 2, 9, 4, 7, 2, 5]
e = [4, 2, 9, 7, 5]
r = dedup(l)
print(r)