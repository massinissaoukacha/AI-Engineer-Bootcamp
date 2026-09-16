from decimalToBinary import decimalToBinary

def BitCounting(n):
    return decimalToBinary(n).count("1")

"""
    def count_bits(n):
        cbits = 0
        while n >= 1 :
            rest = n % 2
            if rest == 1 :
                cbits +=1
            n //=2
        return cbits

"""