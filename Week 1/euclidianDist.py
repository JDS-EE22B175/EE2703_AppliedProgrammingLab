def sq_dist(t1, t2):
    dist = 0

    for i in range(0, len(t1)):
        dist = (t1[i] - t2[i])**2 + dist
    return dist

print(sq_dist((5,5,5), (0,0,0)))