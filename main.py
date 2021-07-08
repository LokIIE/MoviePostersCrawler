import logging
from models.GlobalConfig import GlobalConfig
from models.Poster import Poster
from operations.Crawler import Crawler
from operations.OutputCsv import OutputCsv
from operations.OutputReport import OutputReport
from operations.OutputSql import OutputSql
logging.basicConfig(level=logging.INFO, filename='crawler-process.log', format='%(asctime)s %(message)s')

config = GlobalConfig("config.ini")
crawler = Crawler(config)
try:
    logging.info("---------- START : process launched ----------")
    crawler.run()
    crawlerStatus = crawler.getStatus()
    
    csvOuput = OutputCsv(config.getOutputFile())
    csvOuput.run(crawlerStatus)

    logging.info("---------- END : %d posters have been found ----------" % crawler.getStatus().countPostersCompleted())

    OutputReport().run(crawlerStatus)
    
except Exception:
    logging.fatal("Fatal error in main", exc_info=True)
