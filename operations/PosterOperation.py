import logging
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

# Extract the poster image link from the poster page URL
class PosterPageOperation:

    def __init__(self, posterInstance, posterImageSelector):
        self._posterInstance = posterInstance
        self._posterImageSelector = posterImageSelector

    # For a poster, get the poster movie name
    def run(self):
        img = self.findPosterLink(self._posterInstance.getPosterPageUrl())
        if img:
            logging.debug(img)
            self._posterInstance.setPosterUrl(img)
            posterTitle = self._posterInstance.getPosterTitle().split('-')
            self._posterInstance.setMovieTitle(' '.join(posterTitle))

    def findPosterLink(self, url):
        # Open the URL and read the whole page
        html = urllib.request.urlopen(url).read()
        # Parse the string
        soup = BeautifulSoup(html, 'html.parser')
        # Retrieve the item we were looking for
        tag = soup.select_one(self._posterImageSelector)
        tagsrc = tag.get('src', None)

        return tagsrc