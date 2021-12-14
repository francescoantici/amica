import json
import requests
from models.MargotSentence import MargotSentence
import os

class Paper:
    
    source = ""
    
    def __init__(self, title, authors, published, link, summary = None, pdf = None, margotSentences = [], key = None):
        self.title = title
        self.authors = authors
        self.published = published
        self.link = link 
        self.pdf = pdf
        self.summary = summary
        if key is None:
            self.key = self._generateKey()
        else:
            self.key = key
        self.margotSentences = margotSentences
        
    def getText(self):
        return "\n".join([margotSentence.text for margotSentence in self.margotSentences])
    
    def _generateKey(self):
        return self.source + "_" + self.link.split("/")[-1]
        
    @staticmethod
    def fromXml(entry):
        pass
    
    @staticmethod
    def fromBson(bson):
        paper = Paper(title = bson['title'], authors = bson['authors'], published = bson['published'], link = bson['link'], 
                     summary = bson['summary'], pdf = bson['pdf'], margotSentences = [MargotSentence.fromBson(entry) for entry in bson['margotSentences']], key = bson['key'])
        paper.source = bson['source']
        return paper
    
    def toJson(self):
        d = self.__dict__
        d['source'] = self.source
        d['margotSentences'] = [sentence.__dict__ for sentence in self.margotSentences]
        return json.dumps(d)
    
    def toPdf(self, path):
        fileP = os.path.join(path, self.key+".pdf")
        if os.path.isfile(fileP):
            print("{} already existing!".format(fileP))
            return True
        try:
            response = requests.get(self.pdf)
        except Exception as e:
            print(e)
            return False
        else:
            with open(fileP, "wb") as f:
                f.write(response.content)
            print("saved {} in {}".format(self.key, fileP))
            return True
    
    def toDb(self):
        d = self.__dict__
        d['source'] = self.source
        d['margotSentences'] = [margotSentence.__dict__ for margotSentence in self.margotSentences] 
        return d 
    
    def toHtml(self):
        pass
    
    
    
  
            