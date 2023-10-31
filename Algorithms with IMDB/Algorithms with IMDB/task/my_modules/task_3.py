def bubble_sort_movies(movie_list, order="ascending"):
    """
    Will sort a movie, rating paired list in place.
    """
    swapped = True
    last_bubble_sort_index = len(movie_list) - 1
    while swapped:
        swapped = False
        for i in range(last_bubble_sort_index):
            movie1 = movie_list[i]
            movie2 = movie_list[i + 1]
            relative_order = _determine_pair_order(movie1, movie2)
            if relative_order not in {order, "equal"}:
                swapped = True
                _swap_elements_in_array(movie_list, i, i + 1)
        last_bubble_sort_index -= 1


def _determine_pair_order(movie1: list, movie2: list):
    """
    Returns ascending, descending, or equal based on rating comparison
    """
    rating1 = float(movie1[1])
    rating2 = float(movie2[1])
    if rating1 > rating2:
        return "descending"
    elif rating2 > rating1:
        return "ascending"
    else:
        return "equal"


def _swap_elements_in_array(array: list, index1: int, index2: int):
    """
    Will swap two elements of an array in place.
    """
    temp = array[index1]
    array[index1] = array[index2]
    array[index2] = temp
