from pymongo import MongoClient

class MongoDbInstance:
     
    def __init__(self, host, dbName, verbose = False):
        client = MongoClient(host)
        self.db = client[dbName]
        if verbose:
            print("Connection to db {} completed sucessfully".format(dbName))
    
    def insertDocument(self, doc):
        try:
            result = self.db.papers.insert_one(doc)
        except Exception as e:
            print(e)
            return False
        else:
            print("Document {} inserted successfully".format(result.inserted_id))
            return True
        
    def insertDocuments(self, docList):
        try:
            result = self.db.papers.insert_many(docList)
        except Exception as e:
            print(e)
            return False
        else:
            print("Documents inserted successfully")
            #return result.inserted_ids
            return True
    
    def find(self, query):
        if not(isinstance(query, dict)):
            return []
        return self.db.papers.find(query)

    def getPapersKey(self):
        return [paper['key'] for paper in self.db.papers.find()]
    
    def getPapers(self):
        return self.db.papers.find()
        
            
        
    
    
     