def quick_sort(array):
    if len(array) == 0 :
        return []

    if len(array) == 1 :
        return [array[0]]
        
    pivot = array[0]  # or pivot = array[-1] le dernier
    left_part = [item for item in array if item < pivot]
    right_part = [item for item in array if item > pivot]
    eq_part = [item for item in array if item == pivot]

    sorted_left_part = quick_sort(left_part)
    sorted_right_part = quick_sort(right_part)

    sorted_array = sorted_left_part + eq_part + sorted_right_part
    return sorted_array

print(quick_sort([20, 3, 14, 1, 5]))