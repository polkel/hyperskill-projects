# From a sorted list of movie and rating pairs, return all movies with a certain rating
# Use binary search principles
# Algorithm:
# - Use binary search to find first instance of target rating
# - Use low and high index of that window to create two new windows
# - Use function find_high_edge and find_low_edge that will be symmetrical in function
# - find_high_edge will take a window. Base case will be low == high
# - target rating will always be set by low index
# - if mid is target rating, new window is mid to high
# - if mid is not target rating, new window will be low to mid - 1

def find_movie_rating(sorted_list: list, rating: float):
    """
    Return low and high index of a list of movie and rating pairs with a specific rating.
    Returns empty dict if rating is not in the given list.
    """
    index_dict = dict()
    rating_dict = _rating_search_binary(sorted_list, rating)
    if rating_dict:
        index_dict["low"] = _find_low_edge(sorted_list, rating, rating_dict["low"], rating_dict["mid"])
        index_dict["high"] = _find_high_edge(sorted_list, rating, rating_dict["mid"], rating_dict["high"])
    return index_dict


def _rating_search_binary(sorted_list: list, rating: float, low=0, high=None):
    """
    Takes a sorted list of movie and rating pairs, finds the target rating with binary search.
    If rating is present, returns a dict of low, mid, and high indices, mid is the index of the queried rating.
    Otherwise, returns an empty dict.
    """
    search_dict = dict()

    if not high:
        high = len(sorted_list) - 1
    mid = (low + high) // 2
    mid_number = float(sorted_list[mid][1])
    if mid_number == rating:  # base case, we found the rating
        search_dict["low"] = low
        search_dict["high"] = high
        search_dict["mid"] = mid
        return search_dict
    elif low > high:  # base case that there is no matching rating
        return search_dict
    else:
        if mid_number > rating:  # search lower window
            high = mid - 1
        else:  # search higher window
            low = mid + 1
        return _rating_search_binary(sorted_list, rating, low, high)


def _find_high_edge(sorted_list: list, rating: float, low: int, high: int):
    """
    Finds the highest index in sorted_list where sorted_list[low][1] occurs
    """
    mid = (low + high) // 2
    mid_number = float(sorted_list[mid][1])
    if high - low < 2:  # base case that we've found the last occurring rating
        if float(sorted_list[high][1]) == rating:
            return high
        else:
            return low
    if mid_number == rating:
        low = mid
    else:
        high = mid - 1
    return _find_high_edge(sorted_list, rating, low, high)


def _find_low_edge(sorted_list: list, rating: float, low: int, high: int):
    """
    Same as _find_high_edge, but for finding the lower edge
    """
    mid = (low + high) // 2
    mid_number = float(sorted_list[mid][1])
    if high - low < 2:
        if float(sorted_list[low][1]) == rating:
            return low
        else:
            return high
    if mid_number == rating:
        high = mid
    else:
        low = mid + 1
    return _find_low_edge(sorted_list, rating, low, high)
