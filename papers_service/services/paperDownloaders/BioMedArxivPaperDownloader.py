from services.paperDownloaders.IPaperDownloader import IPaperDownloader
from models.BioMedArxivPaper import BioMedArxivPaper
import time
import json

class BioMedArxivPaperDownloader(IPaperDownloader):
    
    @classmethod
    def getPapers(cls, start = 0):
        count = 30
        baseUrl = "https://api.biorxiv.org/covid19/{}/json".format(start)
        time.sleep(1)
        res = json.loads(cls.request(baseUrl, method = "post"))
        if res["messages"][0]["total"] <= start + count:
            return cls.parseResponse(res)
        return cls.parseResponse(res) + cls.getPapers(start = start + count)
    
    @classmethod
    def parseResponse(cls, response):
        return [BioMedArxivPaper.fromJson(item) for item in response["collection"]]
        
        
    
            
        