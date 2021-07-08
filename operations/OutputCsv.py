import csv, logging
from models.CrawlerStatus import CrawlerStatus 
from models.Poster import Poster

class OutputCsv:

    def __init__(self, filename: str):
        self._filename = filename + ".csv"

    def getFilename(self) -> str:
        return self._filename

    def run(self, crawlerStatus: CrawlerStatus):
        logging.info("---------- OUPUT : export result to CSV file %s ----------" % self.getFilename())
        results = crawlerStatus.getCompletedResults()

        with open(self.getFilename(), 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            writer.writerow(["imdbId", "movieTitle", "posterUrl", "posterTitle", "posterPageUrl", "movieUrl"])
            
            for result in results:
                poster: Poster = result
                writer.writerow(poster.serialize())