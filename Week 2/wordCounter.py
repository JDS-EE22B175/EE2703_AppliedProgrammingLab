def word_count(s):
    wordCount = 0
    if (len(s) == 0): 
        return wordCount
    
    if(s[0].isspace() == False):
        wordCount += 1

    for i in range(1, len(s)):
        if (s[i].isspace() == True and s[i-1].isspace() != True):
            wordCount += 1
    return wordCount

print(word_count(""))