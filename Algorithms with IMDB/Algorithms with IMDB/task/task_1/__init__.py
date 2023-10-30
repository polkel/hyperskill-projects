import csv
import os

_module_dir = os.path.dirname(__file__)


def extract_movie_csv(file_name: str):
    """
    Converts a csv of movie and movie ratings to a list of lists.

    :param str file_name: The file name of the csv in the supplemental_data folder
    :return: A list of paired movie and rating strings e.g. [movie_name, rating]
    """
    _set_correct_directory()
    movie_list = []
    with open(file_name, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            movie_list.append(row)
    return movie_list


def _set_correct_directory():
    """
    Sets correct starting directory relative to this module
    """
    os.chdir(_module_dir)
    os.chdir("..")
    os.chdir("supplemental_data")


def read_movie_list(movie_list: list):
    """
    Takes movie list output from extract_movie_csv and returns a string of movies and ratings separated by '-'
    :param list movie_list:
    :return: string of movies and ratings separated by a hyphen
    """
    movie_string = ""
    for movie in movie_list:
        movie_string += f"{movie[0]} - {movie[1]}\n"
    return movie_string
