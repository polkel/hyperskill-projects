def solution2(x, y):
    set_x = set(x)
    set_y = set(y)
    if len(set_x) > len(set_y):
        unique_num = set_x.difference(set_y).pop()
    else:
        unique_num = set_y.difference(set_x).pop()
    return unique_num
