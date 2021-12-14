from services.database.MongoDbInstance import MongoDbInstance
from models.MargotSentence import MargotSentence
from models.Paper import Paper
from models.Body import Body
from models.Query import Query
from utils.margotSentences.sorting import SortingFunctions
import os
import time
import argparse
import sys

def main(dbHost, dbName, query, htmlPath = None):
    db = MongoDbInstance(host = dbHost, dbName = dbName)
    papers = [Paper.fromBson(entry) for entry in db.getPapers()]
    queryWords = Query(query = query)
    #ALGORITMO DI MATCH QUERY --> PAPERS score medio di evidence_score maggiore
    #sortedResults = SortingFunctions.sortByAverageEvidenceScore(papers)
    sortedResults = SortingFunctions.sortByCorrespondance(papers, query=queryWords)
    print(Body.createHTML(resultList = sortedResults, htmlPath = htmlPath, query = query))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", action="store", help="query string", required = True)
    parser.add_argument("--dbName", "-dn", action="store", help="Name of the db", required = True)
    parser.add_argument("--dbHost", "-dh", action="store", help="Host of the db", required = True)
    parser.add_argument("--htmlPath", "-hp", action="store", help="Host of margot analysed html files", required = True)
    args = parser.parse_args()
    main(query = args.query, dbHost = args.dbHost, dbName = args.dbName, htmlPath = args.htmlPath)
    
    

    

    
  