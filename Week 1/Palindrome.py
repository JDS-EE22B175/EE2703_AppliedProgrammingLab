import math

def palindrome(s):
    isPalindrome = True  #  Assuming all strings are Palindromes until proven otherwise
    newString = str()  #  Creating an empty string
    for i in range(0, len(s)):
        if(ord(s[i]) in range(97,123) or ord(s[i]) in range(48,58) or ord(s[i]) in range(65,91)):  
            #  Checking if each character in the string is a letter or a number
            newString += s[i]  #  If so adding it to a new string that has only letters and numbers
            
    l = len(newString)  #  Finding the length of the new string
    newString = newString.lower()  #  Converting the new string to lower case
    for i in range(0, math.floor(l/2)):
        if(newString[i] != newString[l - i - 1]):  #  Checking if it is not a Palindrome
            isPalindrome = False  #  If it is not a palindrome
            break  #  Then break
            
    return isPalindrome

print(palindrome("A man, a plan, a canal. Panama!"))