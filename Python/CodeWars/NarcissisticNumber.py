def narcissistic( value ):
    toString = str(value)
    nbrDigits = len(toString)
    return value == sum(list(map(lambda d : int(d) ** nbrDigits, toString)))