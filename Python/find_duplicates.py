from collections import Counter

def find_duplicates(nums):
    counter_nums = Counter(nums)
    return [num for num in counter_nums if counter_nums[num] > 1]

print(find_duplicates([1, 2, 3, 2, 3, 4, 5]))