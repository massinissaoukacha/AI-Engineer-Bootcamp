def get_sum(a,b):
    if a == b :
        return a
    else:
        if a > b :
            c = b
            b = a
            a = c
        return sum([x for x in range(a, b+1)])

print(get_sum(-542,2160))