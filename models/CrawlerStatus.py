class CrawlerStatus:

    def __init__(self, startUrl):
        self._pageCount = 1
        self._currentPage = startUrl
        self._results = []

    def getCurrentPage(self):
        return self._currentPage

    def getResults(self):
        return self._results

    def addResult(self, result):
        self.getResults().append(result)
        return self

    def getPageCount(self):
        return self._pageCount

    def addPageCount(self, nbPage):
        self._pageCount += nbPage