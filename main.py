from models.GlobalConfig import GlobalConfig
from operations.Crawler import Crawler
from models.Poster import Poster
import csv
import logging
logging.basicConfig(level=logging.INFO, filename='crawler-process.log', format='%(asctime)s %(message)s')

logging.info("---------- SETUP : loading configuration ----------")
config = GlobalConfig("config.ini")
crawler = Crawler(config)
try:
    with open(config.getOutputFile(), 'w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(["movieTitle", "posterUrl", "posterTitle", "posterPageUrl", "movieUrl"])
        crawler.setWriter(writer)
        logging.info("---------- START : process launched ----------")
        crawler.run()

    logging.info("---------- END : %d posters have been found ----------" % crawler.getStatus().countPostersCompleted())
    crawler.getStatus().logExecutionReport()
    
except Exception:
    logging.fatal("Fatal error in main", exc_info=True)