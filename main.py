from models.GlobalConfig import GlobalConfig
from operations.Crawler import Crawler
from models.Poster import Poster
import csv
import logging
logging.basicConfig(level=logging.INFO)

logging.info("---------- SETUP : loading configuration ----------")
config = GlobalConfig("config.ini")
crawler = Crawler(config)
with open(config.getOutputFile(), 'w', newline='', encoding='utf-8') as output:
    writer = csv.writer(output)
    writer.writerow(["movieTitle", "posterUrl", "posterTitle", "posterPageUrl"])
    crawler.setWriter(writer)
    logging.info("---------- START : process launched ----------")
    crawler.run()

posters = crawler.getStatus().getResults()
logging.info("---------- END : %d posters have been found ----------" % (len(posters)))