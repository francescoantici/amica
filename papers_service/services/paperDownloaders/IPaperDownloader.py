import abc
import requests
import xml.etree.ElementTree as ET
import json

class IPaperDownloader(abc.ABC):
    
    @staticmethod
    def parseXmlResponse(response):
        return ET.fromstring(response)
    
    @staticmethod
    def parseJsonResponse(response):
        return json.loads(response)
    
    @classmethod
    @abc.abstractclassmethod
    def parseResponse(cls, response):
        pass
    
    @classmethod
    @abc.abstractclassmethod
    def getPapers(cls, topic, start, max_results):
        pass
    
    @staticmethod
    def request(baseUrl, params = None, headers = None, method = "get"):
        try:
            response = requests.request(method, url = baseUrl, params = params, headers = headers)
        except Exception as e:
            print(e)
            return False
        else:
            return response.content
    
    @classmethod
    def getOtherPaper(cls, paperCollected, paperAvailable):
        #paperCollected = offset
        if paperAvailable == paperCollected:
            return
        else:
            return cls.getPapers()
            
    
    
    
    