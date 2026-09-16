def two_sum(numbers, target):
    i = 0 # index
    length = len(numbers)
    while i < length :
        number1 = numbers[i]
        number2 = target - number1
        if number2 != number1:
            if number2 in numbers:
                return numbers.index(number1), numbers.index(number2)
            else : i +=1
        else :
            if numbers.count(number1) == 1 : i +=1
            else :
                indexes = tuple(j for j, v in enumerate(numbers) if v == number1)
                return indexes[:2]