import copy


def solve(obj):
    return not id(obj) == id(copy.copy(obj))