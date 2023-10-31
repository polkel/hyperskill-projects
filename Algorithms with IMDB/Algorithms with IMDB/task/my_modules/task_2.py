def find_rating_linear(movie_list: list, rating: float):
    """
    Returns indices of movies from movie list with a matching rating
    """
    matching_ratings = []
    for i in range(len(movie_list)):
        if rating == float(movie_list[i][1]):
            matching_ratings.append(i)
    return matching_ratings
