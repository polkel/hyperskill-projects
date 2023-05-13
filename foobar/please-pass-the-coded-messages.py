# Algo:
# 1. Sort list from largest to smallest
# 2. Sum all digits together
# 3. Find the sum's remainder with 3
# 4. If there's a remainder, see if a digit can be taken out to make the digits divisible by 3 (pass to helper func)
# 5. If no remainder, pass the current set of digits to be made into a large number
# 6. If there's no way to make it divisible by 3, then return 0
#
# Algo to make digits divisible by 3:
# 1. Create a list of digits with remainder of 1 with 3 [1, 4, 7]
# 2. Create a list of digits with remainder of 2 with 3 [2, 5, 8]
# 3. With remainder, look through appropriate list and try to remove 1 digit
# 4. If not in first list, look through second list and try to remove 2 digits
# 5. Return resulting list

def solution(l):
    l_copy = l[:]
    l_copy.sort(reverse=True)
    l_sum = sum(l_copy)
    remainder = l_sum % 3
    if remainder:
        l_copy = make_divisible(l_copy, remainder)
    if not l_copy:
        return 0
    large_num_str = str(l_copy).strip("[]").replace(", ", "")
    large_num = int(large_num_str)
    return large_num


def make_divisible(l, remainder):
    rem_1 = [1, 4, 7]
    rem_2 = [2, 5, 8]

    first_list = rem_1
    second_list = rem_2

    if remainder == 2:
        first_list = rem_2
        second_list = rem_1

    for num in first_list:
        if num in l:
            l.remove(num)
            return l

    to_remove = []
    for num in second_list:
        if num in l:
            num_count = l.count(num)
            for _ in range(num_count):
                to_remove.append(num)
        if len(to_remove) >= 2:
            for remove_num in to_remove[:2]:
                l.remove(remove_num)
            return l
    return False
