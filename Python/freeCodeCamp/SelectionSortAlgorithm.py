def selection_sort(array):
    if len(array) == 0 :
        return []
    if len(array) == 1:
        return array

    for i in range(len(array)):
        current_item = array[i]
        small = min(array[i:])
        if current_item != small:
            index = array[i:].index(small) + i
            array[i] = small
            array[index] = current_item

    return array

    """
    current_item = array[0]
    small = min(array)
    if current_item != small :
        index = array.index(small)
        array[0] = small
        array[index] = current_item

    return array[0:1] + selection_sort(array[1:])
    """
print(selection_sort([1, 4, 2, 8, 345, 123, 43, 32, 5643, 63, 123, 43, 2, 55, 1, 234, 92]))