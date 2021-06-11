class Poster:

    count = 0

    def __init__(self):
        self._posterPageUrl = ""
        self._posterUrl = ""
        self._posterTitle = ""
        self._movieTitle = ""
        self._movieUrl = ""
        self.count += 1

    def getPosterPageUrl(self):
        return self._posterPageUrl

    def setPosterPageUrl(self, url):
        self._posterPageUrl = url
        return self
        
    def getPosterUrl(self):
        return self._posterUrl

    def setPosterUrl(self, url):
        self._posterUrl = url
        return self

    def getPosterTitle(self):
        return self._posterTitle

    def setPosterTitle(self, title):
        self._posterTitle = title
        return self

    def getMovieTitle(self):
        return self._movieTitle

    def setMovieTitle(self, title):
        self._movieTitle = title
        return self

    def getMovieUrl(self):
        return self._movieUrl

    def setMovieUrl(self, url):
        self._movieUrl = url
        return self

    def serialize(self):
        return [self.getMovieTitle(), self.getPosterUrl(), self.getPosterTitle(), self.getPosterPageUrl()]
        
    
