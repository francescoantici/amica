from services.paperDownloaders.IPaperDownloader import IPaperDownloader
from models.ArxivPaper import ArxivPaper
import time

class ArxivPaperDownloader(IPaperDownloader):
    
    namespaces = {
        "feed" : "http://www.w3.org/2005/Atom",
        "arxiv" : "http://arxiv.org/schemas/atom",
        "opensearch" : "http://a9.com/-/spec/opensearch/1.1/" 
    }
    
    @classmethod
    def getPapers(cls, topic = "covid", start = 0, max_results = 100):
        baseUrl = 'http://export.arxiv.org/api/query?'
        params = {"search_query" : topic, "start" : start, "max_results" : max_results}
        time.sleep(1)
        res = cls.request(baseUrl = baseUrl, params = params)
        xml = IPaperDownloader.parseXmlResponse(res)
        if int(xml.find('opensearch:totalResults', cls.namespaces).text) <= (start + max_results):
            return cls.parseResponse(xml)
        return cls.parseResponse(xml) + cls.getPapers(topic = topic, start = start+max_results, max_results = max_results)
        
    
    @classmethod
    def parseResponse(cls, response):
        return [ArxivPaper.fromXml(entry, cls.namespaces) for entry in response.findall('feed:entry', cls.namespaces)]


        