import logging
import urllib.request, urllib.parse, urllib.error
import json
from models.Poster import Poster
from models.GlobalConfig import GlobalConfig


class SearchMovieOperation:

    def __init__(self, config: GlobalConfig, posterInstance: Poster):
        self._movieSearchApi = config.getMovieSource()['url']
        self._apiKey = config.getMovieSource()['token']
        self._poster = posterInstance

    def getQuery(self, lang='en-US'):
        return self._movieSearchApi + '&language=' + lang + '&query=' + self._poster.getPosterTitle() 

    def getMovieResult(self, json):
        return json['results'][0]

    def getMovieTitle(self, json):
        return json['original_title']

    def getMovieSummary(self, json):
        return json['overview']

    def getMovieId(self, json):
        return json['id']

    def getExternalIdQuery(self, json):
        return 'https://api.themoviedb.org/3/movie/' + str(self.getMovieId(json)) + '/external_ids?api_key=' + self._apiKey

    def getImdbId(self, json):
        return json['imdb_id']

    def getMovieDetails(self):
        movieQuery = self.getQuery()
        # logging.log(logging.DEBUG, movieQuery)
        jsonResponse = json.loads(urllib.request.urlopen(movieQuery).read())
        logging.log(logging.DEBUG, jsonResponse)
        result = self.getMovieResult(jsonResponse)
        logging.log(logging.DEBUG, self._poster.getPosterTitle() + ' => ' + self.getMovieTitle(result))
        return result

    def run(self):
        movieDetails = self.getMovieDetails()
        self._poster.setMovieTitle(self.getMovieTitle(movieDetails))

        externalIdQuery = self.getExternalIdQuery(movieDetails)
        logging.log(logging.DEBUG, externalIdQuery)
        externalIds = json.loads(urllib.request.urlopen(externalIdQuery).read())
        
        logging.log(logging.DEBUG, self.getImdbId(externalIds))

        self._poster.setMovieImdbId(self.getImdbId(externalIds))