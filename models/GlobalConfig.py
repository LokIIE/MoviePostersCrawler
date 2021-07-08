import configparser, logging

class GlobalConfig:

    def __init__(self, file):
        logging.info("---------- SETUP : loading configuration ----------")
        self.config = configparser.ConfigParser()
        self.config.read(file)

        self._postersSource = self.config["Posters source"]
        self._movieSource = self.config["Movie source"]
        self._database = self.config["database"]
        
    def getPostersSource(self):
        return self._postersSource

    def getMovieSource(self):
        return self._movieSource

    def getDatabase(self):
        return self

    def getOutputFile(self) -> str:
        return self.config["process"]["output"]
        
    def getNbScanWorkers(self) -> int:
        return int(self.config["process"]["nbScanWorkers"])

    def getNbDataWorkers(self) -> int:
        return int(self.config["process"]["nbDataWorkers"])

    def getMaxPosterPageCount(self) -> int:
        if self.config["process"]["maxPosterPageCount"] == '':
            return None
        
        count = int(self.config["process"]["maxPosterPageCount"])

        if count <= 0:
            return None

        return count

    def getMaxPosterCount(self) -> int:
        if self.config["process"]["maxPosterCount"] == '':
            return None
        
        count = int(self.config["process"]["maxPosterCount"])

        if count <= 0:
            return None

        return count
