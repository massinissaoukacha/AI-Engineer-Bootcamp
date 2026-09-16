def persistence(n):
    if n < 10 and n >=0 : 
        return 0
    else :
        s = str(n)
        n = 1
        for c in s:
            n *= int(c)    
        return 1 + persistence(n)