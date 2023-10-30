import task_1


MOVIE_FILE_NAME = "movies.csv"


movie_list = task_1.extract_movie_csv(MOVIE_FILE_NAME)
movie_string = task_1.read_movie_list(movie_list)
print(movie_string)
