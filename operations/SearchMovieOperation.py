import logging
import urllib.request, urllib.parse, urllib.error
import json
from models.Poster import Poster
from models.GlobalConfig import GlobalConfig
from models.PosterDataStatus import PosterDataStatus

class SearchMovieOperation:

    def __init__(self, config: GlobalConfig, posterInstance: Poster):
        self._movieSearchApi = config.getMovieSource()['url']
        self._apiKey = config.getMovieSource()['token']
        self._poster = posterInstance

    def getQuery(self, lang='en-US'):
        return self._movieSearchApi + '&language=' + lang + '&query=' + self._poster.getPosterTitle() 

    def getMovieResult(self, json):
        if not json['results']:
            return None

        if len(json['results']) == 0:
            return None
            
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
        jsonResponse = json.loads(urllib.request.urlopen(movieQuery).read())
        result = self.getMovieResult(jsonResponse)
        
        return result

    def run(self):
        try:
            movieDetails = self.getMovieDetails()
        except:
            logging.error('Poster %s : Error while searching for movie %s details (query: %s)', self._poster.getPosterTitle(), self._poster.getPosterTitle(), self.getQuery())
            self._poster.setStatus(PosterDataStatus.MOVIE_DETAILS_NOT_FOUND)
            return

        if movieDetails == None:
            logging.warning('Poster %s : Movie "%s" => no result (%s)', self._poster.getPosterTitle(), self._poster.getPosterTitle(), self.getQuery())
            self._poster.setStatus(PosterDataStatus.MOVIE_DETAILS_NOT_FOUND)
            return
        
        self._poster.setMovieTitle(self.getMovieTitle(movieDetails))
        self._poster.setStatus(PosterDataStatus.MOVIE_DETAILS_FOUND)
        logging.debug('%s => %s', self._poster.getPosterTitle(), self.getMovieTitle(movieDetails))

        externalIdQuery = self.getExternalIdQuery(movieDetails)
        try:
            externalIds = json.loads(urllib.request.urlopen(externalIdQuery).read())
        except:
            logging.error('Poster %s : Error while searching for movie %s Imdb Id (query: %s)', self._poster.getPosterTitle(), self._poster.getMovieTitle())
            self._poster.setStatus(PosterDataStatus.IMDB_ID_NOT_FOUND)
            return
        
        if not self.getImdbId(externalIds):
            self._poster.setStatus(PosterDataStatus.IMDB_ID_NOT_FOUND)
            logging.warning('Poster %s : Imdb id not found in %s', self._poster.getPosterTitle(), externalIds)
            return
            
        self._poster.setMovieImdbId(self.getImdbId(externalIds))
        self._poster.setStatus(PosterDataStatus.COMPLETE)
        logging.debug('Poster %s : %s => ImdbId : %s', self._poster.getPosterTitle(), self.getMovieTitle(movieDetails), self.getImdbId(externalIds))