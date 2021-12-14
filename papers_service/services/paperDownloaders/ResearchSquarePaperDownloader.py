from services.paperDownloaders.IPaperDownloader import IPaperDownloader
from models.ResearchSquarePaper import ResearchSquarePaper
import subprocess
import time

class ResearchSquarePaperDownloader(IPaperDownloader):
    
    @classmethod
    def getPapers(cls, topic = "covid", start = 0, max_results = 100):
        baseUrl = "https://www.researchsquare.com/api/search"
        params = {"unified":topic, "offset":start, "limit":max_results}
        try:
            #res = subprocess.check_output("curl GET {}?keyword={}&journal={}&offset={}&limit={}".format(baseUrl, topic, "ResearchSquare", start, max_results), shell=True).decode('utf-8')
            time.sleep(1)
            res = cls.request(baseUrl, params = params)
        except Exception as e:
            print(e)
            return
        json = cls.parseJsonResponse(res)['result']
        if int(json['total']) <= start + max_results:
            return cls.parseResponse(json)
        return cls.parseResponse(json) + cls.getPapers(topic = topic, start = start + max_results, max_results= max_results)
    
    @classmethod
    def parseResponse(cls, response):
        json = response['data']
        return [ResearchSquarePaper.fromJson(elem) for elem in json]