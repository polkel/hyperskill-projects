def merge_sort_movie_list(movie_list: list, left=0, right=None):
    """
    Sorts a movie and rating list with the merge sort algorithm (ascending).
    Changes the order of the input list.
    """
    if right is None:
        right = len(movie_list) - 1
    if left < right and not right - left == 1:
        mid = (left + right) // 2
        merge_sort_movie_list(movie_list, left, mid - 1)
        merge_sort_movie_list(movie_list, mid, right)
        _merge(movie_list, left, mid, right)
    elif right - left == 1:
        _merge(movie_list, left, right, right)


def _merge(movie_list, left, mid, right):
    """
    Merges two sorted arrays (movie_list[left: mid] and movie_list[mid: right + 1] and places them
    in a sorted order within movie_list
    """
    left_array = movie_list[left: mid]
    right_array = movie_list[mid: right + 1]
    left_count = 0
    right_count = 0
    list_count = left
    while left_count < len(left_array) and right_count < len(right_array):
        left_value = float(left_array[left_count][1])
        right_value = float(right_array[right_count][1])
        if left_value <= right_value:
            movie_list[list_count] = left_array[left_count]
            left_count += 1
        else:
            movie_list[list_count] = right_array[right_count]
            right_count += 1
        list_count += 1

    while left_count < len(left_array):
        movie_list[list_count] = left_array[left_count]
        left_count += 1
        list_count += 1

    while right_count < len(right_array):
        movie_list[list_count] = right_array[right_count]
        right_count += 1
        list_count += 1
