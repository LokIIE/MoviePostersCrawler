import logging
from models.CrawlerStatus import CrawlerStatus 
from models.Poster import Poster

class OutputSql:

    def __init__(self, filename: str):
        self._filename = filename + ".sql"

    def getFilename(self) -> str:
        return self._filename

    def run(self, crawlerStatus: CrawlerStatus):
        logging.info("---------- OUPUT : export result to SQL file %s ----------" % self.getFilename())
        results = crawlerStatus.getCompletedResults()

        lines = [
            "INSERT INTO list_posters (imdb_id, poster_title, poster_storepage, poster_image, movie_title, movie_url)\n",
            "VALUES\n"
        ]

        for result in results:
            poster: Poster = result
            lines.append(
                '("%s", "%s", "%s", "%s", "%s", "%s")\n' % (
                poster.getImdbId(),
                poster.getPosterTitle(),
                poster.getPosterPageUrl(),
                poster.getPosterUrl(),
                poster.getMovieTitle(),
                poster.getMovieUrl()
            ))
        
        with open(self.getFilename(), 'w', newline='', encoding='utf-8') as output:
            output.writelines(lines)
