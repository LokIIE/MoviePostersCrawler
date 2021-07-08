import logging
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from models.GlobalConfig import GlobalConfig
from models.Poster import Poster
from models.PosterDataStatus import PosterDataStatus

# Extract the poster image link from the poster page URL
class PosterPageOperation:

    def __init__(self, config: GlobalConfig, posterInstance: Poster):
        self._posterImageSelector = config.getPostersSource()['posterImageSelector']
        self._posterInstance = posterInstance

    # For a poster, get the poster movie name
    def run(self):
        img = self.findPosterLink(self._posterInstance.getPosterPageUrl())
        if not img:
            self._posterInstance.setStatus(PosterDataStatus.POSTER_DETAILS_NOT_FOUND)
            logging.warning('Poster %s : details not found (url: %s)', self._poster.getPosterTitle(), self._posterInstance.getPosterPageUrl())
            return

        logging.debug(img)
        self._posterInstance.setPosterUrl(img)
        posterTitle = self._posterInstance.getPosterTitle().split('-')
        self._posterInstance.setMovieTitle(' '.join(posterTitle))
        self._posterInstance.setStatus(PosterDataStatus.POSTER_DETAILS_FOUND)

    def findPosterLink(self, url: str) -> str:
        # Open the URL and read the whole page
        html = urllib.request.urlopen(url).read()
        # Parse the string
        soup = BeautifulSoup(html, 'html.parser')
        # Retrieve the item we were looking for
        tag = soup.select_one(self._posterImageSelector)
        tagsrc = tag.get('src', None)

        return tagsrc