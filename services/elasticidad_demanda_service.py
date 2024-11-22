
import init_service


class ElasticidadDemandaService(InitService):

    def __init__(self,):
        pass

    def checkDataStatus(self):
        return self.UPTODATE

    def scratchInitialization(self):
        print("ElasticidadDemanda: Initializing from scratch...")

    def updateData(self):
        print("ElasticidadDemanda: Updating data...")

