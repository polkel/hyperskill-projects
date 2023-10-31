from my_modules import *


MOVIE_LIST_FILE = "movies.csv"


movie_list = task_1.extract_movie_csv(MOVIE_LIST_FILE)
task_5.merge_sort_movie_list(movie_list)
rating_range = task_4.find_movie_rating(movie_list, 6.0)
sub_list = movie_list[rating_range["low"]: rating_range["high"] + 1]
movie_string = task_1.read_movie_list(sub_list)
print(movie_string)
