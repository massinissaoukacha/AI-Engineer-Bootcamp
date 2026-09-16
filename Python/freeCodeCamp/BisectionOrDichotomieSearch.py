def square_root_bisection(number, tolerance= 0.01, iterations= 10):
    if number < 0 :
        raise ValueError('Square root of negative number is not defined in real numbers')
    
    if number in (0, 1) :
        print(f'The square root of {number} is {number}')
        return number
    
    low = 0.0
    high = max(1.0, number)
    for i in range(iterations):
        mid = (low + high) / 2
        square = mid ** 2
        #root = None
        #square_target = number
        # number = square_approximately + error | tolerance -> tol = |num - sqr|
        if abs(high - low) < tolerance :
            root = mid
            print(f'The square root of {number} is approximately {root}')
            return root

        elif square > number:
            high = mid
        else :
            low = mid
    
    print(f'Failed to converge within {iterations} iterations')
    return None

square_root_bisection(0.001, 1e-7, 50)