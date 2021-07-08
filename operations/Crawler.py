import logging
import urllib.request, urllib.parse, urllib.error
import concurrent.futures
import queue
import time
import threading
import re
from bs4 import BeautifulSoup
from models.CrawlerStatus import CrawlerStatus
from models.GlobalConfig import GlobalConfig
from models.Poster import Poster
from models.PosterDataStatus import PosterDataStatus
from models.UrlValidator import UrlValidator
from operations.PosterOperation import PosterPageOperation
from operations.SearchMovieOperation import SearchMovieOperation

class Crawler:

    def __init__(self, config: GlobalConfig):
        self._config = config
        self._postersSourceConfig = config.getPostersSource()
        self._baseUrl = self._postersSourceConfig["baseUrl"]
        self._status = CrawlerStatus(self._postersSourceConfig["collection"])
        self._scanningQueue = queue.Queue()
        self._processingQueue = queue.Queue()
        self._result = []
        self._ignoreLinks = []
        self._validator = UrlValidator(self._postersSourceConfig)

    def getStatus(self) -> CrawlerStatus:
        return self._status

    def getResourceUrl(self, resource) -> str:
        return self._baseUrl + resource

    def findLinks(self, queue):
        while True:
            count = 0
            url = self.getResourceUrl(queue.get())
            foundLinks = self.findValidLinks(url)
            for link in foundLinks:
                if self._validator.isSearchPage(link) and not link in self._ignoreLinks and self.checkAddPagesToScan() :
                    self.addPageToScan(link)
                    count += 1
                elif self._validator.isPosterPage(link) and not link in self.getStatus().getResults() and self.checkAddPosterToProcess() :
                    self.addPosterToProcess(link)

            logging.debug("---------- %d new poster pages found ----------" % (count))
            
            queue.task_done()
    
    def checkAddPagesToScan(self) -> bool:
        if self._config.getMaxPosterPageCount() == None:
            return True
        
        return self._config.getMaxPosterPageCount() > self.getStatus().getPageCount()

    def addPageToScan(self, link: str):
        self._scanningQueue.put(link)
        self._ignoreLinks.append(link)
        self.getStatus().addPageCount(1)
        logging.debug("NEW : %s page queued for analysis ..." % (link))

    def checkAddPosterToProcess(self) -> bool:
        if self._config.getMaxPosterCount() == None:
            return True
        
        return self._config.getMaxPosterCount() > len(self.getStatus().getResults())

    def addPosterToProcess(self, link: str):
        poster = Poster()
        poster.setPosterPageUrl(self.getResourceUrl(link))
        poster.setPosterTitle(self.getPosterTitleFromUrl(link))
        poster.setStatus(PosterDataStatus.TO_PROCESS)
        self.getStatus().addResult(poster)
        self._processingQueue.put(poster)

    def getPosterTitleFromUrl(self, url) -> str:
        matchs = re.search(self._postersSourceConfig["posterTitleRegex"], url)
        if matchs:
            return matchs.group(1)

        logging.warning(
            "No poster title regex match for url : %s (regex: %s)" 
            % (url, self._postersSourceConfig["posterTitleRegex"])
        )
        return ""

    def findValidLinks(self, url):
        # Open the URL and read the whole page
        html = urllib.request.urlopen(url).read()
        # Parse the string
        soup = BeautifulSoup(html, 'html.parser')
        # Retrieve all of the anchor tags
        # Returns a list of all the links
        tags = soup('a')

        foundLinks = []

        # Prints all the links in the list tags
        for tag in tags: 
            # Add new links to queue
            link = tag.get('href', None)
            if link == None:
                continue
            if self._validator.isValidPageLink(link):
                foundLinks.append(link)
        
        return foundLinks

    def run(self):
        logging.info(
            "---------- Initializing %d workers for scan, %d for completing information ----------" 
            % (self._config.getNbScanWorkers(), self._config.getNbDataWorkers())
        )

        for _ in range(self._config.getNbScanWorkers()):
            threading.Thread(target=self.findLinks, daemon=True, args=(self._scanningQueue,)).start()

        for _ in range(self._config.getNbDataWorkers()):
            threading.Thread(target=self.findPosterData, daemon=True, args=(self._processingQueue,)).start()

        logging.info("---------- Run crawler ----------")
        
        self._scanningQueue.put(self._status.getCurrentPage())
        self._scanningQueue.join()

        logging.info(
            "---------- Target preliminary scan done, %d posters at most are available on %d pages ----------" 
            % (len(self.getStatus().getResults()), self.getStatus().getPageCount())
        )

        self._processingQueue.join()

        self._status._result = self._result
        return self

    # Complete a poster item with missing data :
    # - poster url
    # - movie title
    def findPosterData(self, queue):
        while True:
            posterInstance: Poster = queue.get()

            PosterPageOperation(self._config, posterInstance).run()
            SearchMovieOperation(self._config, posterInstance).run()

            queue.task_done()
