from models.Poster import Poster
from models.PosterDataStatus import PosterDataStatus
import logging

class CrawlerStatus:

    def __init__(self, startUrl: str):
        self._pageCount = 1
        self._currentPage = startUrl
        self._results = []

    def getCurrentPage(self) -> str:
        return self._currentPage

    def getResults(self) -> list[Poster]:
        return self._results

    def getCompletedResults(self) -> list[Poster]:
        return list(filter(
            lambda poster: poster.getStatus() == PosterDataStatus.COMPLETE,
            self.getResults()
        ))

    def countPostersCompleted(self) -> int:
        return len(self.getCompletedResults())

    def addResult(self, result: Poster):
        self.getResults().append(result)
        return self

    def getPageCount(self) -> int:
        return self._pageCount

    def addPageCount(self, nbPage: int):
        self._pageCount += nbPage
