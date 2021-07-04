from models.Poster import Poster
from models.PosterDataStatus import PosterDataStatus
import logging

class CrawlerStatus:

    def __init__(self, startUrl: str):
        self._pageCount = 1
        self._currentPage = startUrl
        self._results = []

    def getCurrentPage(self):
        return self._currentPage

    def getResults(self) -> list[Poster]:
        return self._results

    def addResult(self, result: Poster):
        self.getResults().append(result)
        return self

    def getPageCount(self):
        return self._pageCount

    def addPageCount(self, nbPage: int):
        self._pageCount += nbPage

    def countPostersCompleted(self) -> int:
        return len(list(
            filter(
                lambda poster: poster.getStatus() == PosterDataStatus.COMPLETE,
                self.getResults()
            )
        ))

    def logExecutionReport(self):
        dictStatusPosters = dict()
        for result in self.getResults():
            poster: Poster = result
            if dictStatusPosters.get(poster.getStatus(), None) == None:
                dictStatusPosters.setdefault(poster.getStatus(), [poster])
            else:
                statusPosters = dictStatusPosters.get(poster.getStatus())
                statusPosters.append(poster)
                dictStatusPosters.update({poster.getStatus(): statusPosters})
        
        for key in dictStatusPosters.keys():
            statusPosters = dictStatusPosters.get(key)
            logging.info('%s : %d', key.name, len(statusPosters))
            if key != PosterDataStatus.COMPLETE:
                for poster in statusPosters:
                    logging.info(' * Poster url: %s; movie : %s', poster.getPosterUrl(), poster.getMovieTitle())