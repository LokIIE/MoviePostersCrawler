from models.PosterDataStatus import PosterDataStatus

class Poster:

    count = 0

    def __init__(self):
        self._imdbId = ""
        self._posterPageUrl = ""
        self._posterUrl = ""
        self._posterTitle = ""
        self._movieTitle = ""
        self._movieUrl = ""
        self.count += 1
        self.status = PosterDataStatus.INIT

    def getStatus(self) -> PosterDataStatus:
        return self.status
        
    def setStatus(self, newStatus: PosterDataStatus):
        self.status = newStatus

    def getPosterPageUrl(self) -> str:
        return self._posterPageUrl

    def setPosterPageUrl(self, url):
        self._posterPageUrl = url
        return self
        
    def getPosterUrl(self) -> str:
        return self._posterUrl

    def setPosterUrl(self, url):
        self._posterUrl = url
        return self

    def getPosterTitle(self) -> str:
        return self._posterTitle

    def setPosterTitle(self, title):
        self._posterTitle = title
        return self

    def getMovieTitle(self) -> str:
        return self._movieTitle

    def setMovieTitle(self, title):
        self._movieTitle = title
        return self

    def getMovieUrl(self) -> str:
        return self._movieUrl

    def setMovieUrl(self, url):
        self._movieUrl = url
        return self

    def getImdbId(self) -> str:
        return self._imdbId

    def setImdbId(self, imdbId: str):
        self._imdbId = imdbId
        self.setMovieImdbId(imdbId)

    def setMovieImdbId(self, imdbId):
        self.setMovieUrl('https://imdb.com/title/' + imdbId)

    def serialize(self) -> list:
        return [self.getMovieTitle(), self.getImdbId(), self.getPosterUrl(), self.getMovieUrl(), self.getPosterPageUrl(), self.getPosterTitle()]
