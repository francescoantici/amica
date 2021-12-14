from services.paperDownloaders.IPaperDownloader import IPaperDownloader

class PubMedPaperDownloader(IPaperDownloader):
    
    @classmethod
    def getPapers(cls, topic, start, max_results):
        ids = cls.searchPapers(topic, start, max_results)
        fetchUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db" : "pubmed", "retmode" : "xml", "id" : ids}
        response = cls.request(baseUrl = fetchUrl, params = params, method = 'post')
        return cls.parseResponse(response)
        
    
    @classmethod
    def searchPapers(cls, topic, start, max_results):
        baseUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db" : "pubmed", "term" : topic, "retstart" : start, "retmax" : max_results}
        response = cls.request(baseUrl = baseUrl, params = params, method = 'post')
        xml = super().parseResponse(response)
        return xml.find('IdList').findall('Id')
    
    @classmethod
    def parseResponse(cls, response):
        xml = cls.parseXmlResponse(response)
        
        
            