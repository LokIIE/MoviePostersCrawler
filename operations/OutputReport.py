import logging
from models.CrawlerStatus import CrawlerStatus
from models.Poster import Poster
from models.PosterDataStatus import PosterDataStatus

class OutputReport:
        
    def run(self, crawlerStatus: CrawlerStatus):
        logging.info("---------- EXECUTION REPORT LOGS ----------")    
        dictStatusPosters = dict()
        
        for result in crawlerStatus.getResults():
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
                    logging.info(
                        ' * movie : %s, poster url: %s' % (
                        poster.getMovieTitle(),
                        poster.getPosterUrl()
                    ))


        logging.info("---------- END EXECUTION REPORT LOGS ----------")
