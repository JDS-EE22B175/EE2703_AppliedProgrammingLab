import math

def dectobase(n, k):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:k] 
    s = ""
    while n > 0:
        s += digits[n % k]  
        n = n // k
    return s[::-1]

print(dectobase(10, 2))