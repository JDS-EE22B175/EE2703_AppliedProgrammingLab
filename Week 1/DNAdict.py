def count_nucleotides(l):
    x = {'A':0, 'G':0, 'C':0, 'T':0, 'Error':0 }
    for i in range(0, len(l)):
        if (l[i] == 'A'): x['A'] = x['A'] + 1
        elif (l[i] == 'G'): x['G'] = x['G'] + 1
        elif (l[i] == 'C'): x['C'] = x['C'] + 1
        elif (l[i] == 'T'): x['T'] = x['T'] + 1
        else: x['Error'] = x['Error'] + 1
        
    return x

x = count_nucleotides("AAGTD")
print(f"{x['A']} {x['G']} {x['T']} {x['C']} {x['Error']}")