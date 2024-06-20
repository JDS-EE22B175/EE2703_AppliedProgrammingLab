def convert_s2c(s):
    newList = []
    i = 0

    if (s[0] != '_'):
        newList.append(s[0].upper())
        i = 1 

    while i < len(s):
        if(s[i] != '_'):
            newList.append(s[i])
            i+=1
        else:
            newList.append(s[i+1].upper())
            i += 2
    newName = "".join(str(element) for element in newList)
    
    return newName

print(convert_s2c("yet_Another_variable"))