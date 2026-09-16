import math

def find_next_square(sq):
    # Return the next square if sq is a square, -1 otherwise
    if sq >= 0 :
        squart = math.isqrt(sq)
        if squart ** 2 != sq : return -1
        else :
            return (squart + 1) ** 2


print(find_next_square(114))