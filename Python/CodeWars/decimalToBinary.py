def decimalToBinary(n):
    binaryChaine = []
    while n >= 1 :
        binaryChaine.append(n%2)
        n //=2
    binaryChaine.reverse()
    return "".join(map(str, binaryChaine))
