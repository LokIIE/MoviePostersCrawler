from enum import Enum

class PosterDataStatus(Enum):
    COMPLETE = 0
    INIT = 1
    TO_PROCESS = 2
    POSTER_DETAILS_FOUND = 3
    POSTER_DETAILS_NOT_FOUND = 4
    MOVIE_DETAILS_FOUND = 5
    MOVIE_DETAILS_NOT_FOUND = 6
    IMDB_ID_NOT_FOUND = 7
