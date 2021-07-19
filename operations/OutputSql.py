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
            "INSERT INTO posters (imdb_id, poster_title, poster_storepage, poster_image, movie_title, movie_url)\n",
            "VALUES\n"
        ]

        for idx, result in enumerate(results):
            poster: Poster = result
            lines.append(
                "('%s', '%s', '%s', '%s', '%s', '%s')" % (
                poster.getImdbId(),
                poster.getPosterTitle(),
                poster.getPosterPageUrl(),
                poster.getPosterUrl(),
                self.formatForPostgres(poster.getMovieTitle()),
                poster.getMovieUrl()
            ))
            if idx == len(results)-1:
                lines.append(';\n')
            else:
                lines.append(',\n')
        
        with open(self.getFilename(), 'w', newline='', encoding='utf-8') as output:
            output.writelines(lines)

    def formatForPostgres(self, value: str) -> str:
        return value.replace("'", "''")
