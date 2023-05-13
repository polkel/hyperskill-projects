import itertools
# Algo:
# 1. Use itertools.combination to create all possible triplets from the list, in current order, no repeats
#    this meets the index requirements of i < j < k
# 2. initialize the count at 0
# 3. loop through iterator. if lucky triple is satisfied, increase count by 1
# 4. return count
#
# Pivot because hidden tests failed due to execution time.
#  1. Create a moving window that skips if the first condition is failed

def solution2(l):
    count = 0

    for index_x, x in enumerate(l[: -2]):
        y_start = index_x + 1
        for index_y, y in enumerate(l[y_start:-1]):
            if y % x != 0:
                continue
            z_start = y_start + index_y + 1
            for z in l[z_start:]:
                if z % y == 0:
                    count += 1

    return count


def solution(l):
    triple_iter = itertools.combinations(l, 3)
    count = 0
    for x, y, z in triple_iter:
        con_1 = y % x == 0
        con_2 = z % y == 0
        if con_1 and con_2:
            count += 1
    return count


def solution3(l):
    count = 0

    for i in range(len(l) - 2):
        for j in range(i + 1, len(l) - 1):
            if l[j] % l[i] != 0:
                continue
            for k in range(j + 1, len(l)):
                if l[k] % l[j] == 0:
                    count += 1

    return count


def solution4(l):
    count = 0

    for i in range(len(l) - 2):
        for j in range(i + 1, len(l) - 1):
            if l[j] % l[i] == 0:
                remaining_matrix = l[j + 1:]
                remaining_set = set(remaining_matrix)
                for num in remaining_set:
                    if num % l[j] == 0:
                        count += remaining_matrix.count(num)

    return count


def solution_working(l):
    count = 0
    divisible_count = []
    for i in range(len(l) - 1):
        divisible = 0
        for num in l[i+1:]:
            if num % l[i] == 0:
                divisible += 1
        divisible_count.append(divisible)
    for i in range(len(l) - 2):
        for j in range(i + 1, len(l) - 1):
            if l[j] % l[i] == 0:
                count += divisible_count[j]

    return count


test_1 = [1, 1, 1]
test_2 = [1, 2, 3, 4, 5, 6]
test_3 = [1] * 2000

print(solution5(test_1))
print(solution5(test_2))
print(solution5(test_3))
