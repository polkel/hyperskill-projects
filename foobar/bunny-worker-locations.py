# Bottom row has a pattern of num(x) = 1 + 2 + 3 + ... + x
# Traversing upwards from bottom row has the same pattern, but has a constant and the series starts at x
# e.g. id(x, y) = num(x)CONSTANT + x + (x + 1) + (x + 2) + ... + (x + (y-2))
# find_sum_series is a helper function that calculates the above
# it uses the premise that if you have a series increasing by 1, you can find the sum of the series
# by averaging the smallest and largest number and multiplying by the length of numbers in the series

def solution(x, y):
    bottom_row_id = find_sum_series(1, x, 0)
    bunny_id = find_sum_series(x, y - 1, bottom_row_id)
    return str(bunny_id)


def find_sum_series(start, n, constant):
    num = ((start + (start + n - 1)) / 2) * n + constant
    return num
