import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import concurrent.futures
import queue
import time
import threading
import re
import logging
from models.CrawlerStatus import CrawlerStatus
from models.GlobalConfig import GlobalConfig
from models.Poster import Poster
from models.UrlValidator import UrlValidator
from operations.PosterOperation import PosterPageOperation

class Crawler:

    def __init__(self, config: GlobalConfig):
        self._config = config
        self._postersSourceConfig = config.getPostersSource()
        self._baseUrl = self._postersSourceConfig["baseUrl"]
        self._status = CrawlerStatus(self._postersSourceConfig["collection"])
        self._scanningQueue = queue.Queue()
        self._processingQueue = queue.Queue()
        self._resultQueue = queue.Queue()
        self._result = []
        self._ignoreLinks = []
        self._validator = UrlValidator(self._postersSourceConfig)

    def getStatus(self):
        return self._status

    def getResourceUrl(self, resource):
        return self._baseUrl + resource

    def findLinks(self, queue):
        while True:
            count = 0
            url = self.getResourceUrl(queue.get())
            foundLinks = self.findValidLinks(url)
            for link in foundLinks:
                if self._validator.isSearchPage(link) and not link in self._ignoreLinks:
                    self._scanningQueue.put(link)
                    self._ignoreLinks.append(link)
                    logging.debug("NEW : %s page queued for analysis ..." % (link))
                    count += 1
                elif self._validator.isPosterPage(link) and not link in self.getStatus().getResults():
                    poster = Poster()
                    poster.setPosterPageUrl(self.getResourceUrl(link))
                    poster.setPosterTitle(self.getPosterTitleFromUrl(link))
                    self.getStatus().addResult(poster)
                    self._processingQueue.put(poster)

            self.getStatus().addPageCount(count)
            logging.debug("---------- %d new poster pages found ----------" % (count))
            
            queue.task_done()
    
    def getPosterTitleFromUrl(self, url):
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
            "---------- Initializing %d workers for scan, %d for completing information and 1 for output ----------" 
            % (self._config.getNbScanWorkers(), self._config.getNbDataWorkers())
        )

        for _ in range(self._config.getNbScanWorkers()):
            threading.Thread(target=self.findLinks, daemon=True, args=(self._scanningQueue,)).start()

        for _ in range(self._config.getNbDataWorkers()):
            threading.Thread(target=self.findPosterData, daemon=True, args=(self._processingQueue,)).start()

        threading.Thread(target=self.processToOutput, daemon=True, args=(self._resultQueue,)).start()

        logging.info("---------- Run crawler ----------")
        
        self._scanningQueue.put(self._status.getCurrentPage())
        self._scanningQueue.join()

        logging.info(
            "---------- Target preliminary scan done, %d posters at most are available on %d pages ----------" 
            % (len(self.getStatus().getResults()), self.getStatus().getPageCount())
        )

        self._processingQueue.join()
        self._resultQueue.join()

        self._status._result = self._result
        return self

    # Complete a poster item with missing data :
    # - poster url
    # - movie title
    def findPosterData(self, queue):
        while True:
            posterInstance = queue.get()
            posterOp = PosterPageOperation(posterInstance, self._postersSourceConfig['posterImageSelector'])
            posterOp.run()
            self._resultQueue.put(posterInstance)
            queue.task_done()

    def processToOutput(self, queue):
        while True:
            posterItem = queue.get()

            self.getWriter().writerow(posterItem.serialize())

            queue.task_done()

    def setWriter(self, writer):
        self._writer = writer

    def getWriter(self):
        return self._writer