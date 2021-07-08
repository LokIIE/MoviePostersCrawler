import re 

class UrlValidator:

    def __init__(self, config):
        self._config = config

    # Url must be a link a new pages with poster or be a link to a movie poster
    def isValidPageLink(self, url) -> bool:
        return self.isPosterPage(url) or self.isSearchPage(url)

    def isPosterPage(self, url) -> bool:
        return re.search(self._config["posterPageRegex"], url) is not None

    def isSearchPage(self, url) -> bool:
        return re.search(self._config["searchPageRegex"], url) is not None
