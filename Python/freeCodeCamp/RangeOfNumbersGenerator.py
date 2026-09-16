def range_of_numbers(start_num, end_num):
    # 2- list of consecutive integers [start_num,...,end_num]
    # 3- start_num <= end_num
    # 6- base case: when start_num == end_num -> return [start_num]
    # 4- recursive case : an argument that moves toward the base case, + the current number to the returned list
    # return end_num + range_of_numbers(start_num, end_num -1)
    if end_num == start_num:
        return [start_num]

    if end_num < start_num:
        current_num = start_num
        start_num = end_num
        end_num = current_num

    current_num = end_num
    end_num -= 1
    return range_of_numbers(start_num, end_num) + [current_num]

print(range_of_numbers(5, 1))