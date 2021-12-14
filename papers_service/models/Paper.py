import json
import requests
from services.textExtractor.TextPdfExtractor import TextPdfExtractor
from models.MargotSentence import MargotSentence
import os
import io
import asyncio

class Paper:
    
    source = ""
    
    def __init__(self, title, authors, published, link, summary = None, pdf = None, margotSentences = []):
        self.title = title
        self.authors = authors
        self.published = published
        self.link = link 
        self.pdf = pdf
        self.summary = summary
        self.key = self._generateKey()
        self.margotSentences = margotSentences
        
    def toDb(self):
        d = self.__dict__
        d['source'] = self.source
        d['margotSentences'] = [margotSentence.__dict__ for margotSentence in self.margotSentences] 
        return d 
    
    def getText(self):
        return "\n".join([margotSentence.text for margotSentence in self.margotSentences])
    
    def _generateKey(self):
        return self.source + "_" + self.link.split("/")[-1]
        
    @staticmethod
    def fromXml(entry):
        pass
    
    @staticmethod
    def fromBson(json):
        return Paper(title = json['title'], authors = json['authors'], published = json['published'], link = json['link'], 
                     summary = json['summary'], pdf = json['pdf'], margotSentences = [MargotSentence.fromBson(entry) for entry in json['margotSentences']])
    
    def toJson(self):
        return json.dumps(self.__dict__)
    
    def toPdf(self, path, fileName = None):
        if fileName is None:
            fileP = os.path.join(path, self.key+".pdf")
        else:
            if not(".pdf" in fileName):
                fileName+=".pdf"
            fileP = os.path.join(path, fileName)
        try:
            response = requests.get(self.pdf, timeout=180)
        except Exception as e:
            print(e)
            return False
        else:
            with open(fileP, "wb") as f:
                f.write(response.content)
            #print("saved {} in {}".format(self.key, fileP))
            return True

    def toBufferedPdf(self):
        try:
            res = requests.get(self.pdf, stream = True)
        except Exception as e:
            print(e)
            return None
        return io.BytesIO(res.content)
    
    
    
    
  
            