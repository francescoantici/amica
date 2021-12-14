from services.paperDownloaders.ArxivPaperDownloader import ArxivPaperDownloader
from services.paperDownloaders.ResearchSquarePaperDownloader import ResearchSquarePaperDownloader
from services.paperDownloaders.BioMedArxivPaperDownloader import BioMedArxivPaperDownloader
from services.textExtractor.TextPdfExtractor import TextPdfExtractor
from services.database.MongoDbInstance import MongoDbInstance
from services.margot.MargotClient import MargotClient
import os
import time
import argparse
import concurrent
import asyncio

def paperPipeline(paper, mg, db):
    try:
        print("*" * 50)
        print("Processing {}".format(paper.key))
        pdf = paper.toBufferedPdf()
        if pdf is None:
            print("Error in analysing {}".format(paper.key))
            return False
        text = TextPdfExtractor.extractFile(fileName = paper.key, data = pdf)
        paper.margotSentences = mg.annotate(text = text, fileName = paper.key)
        db.insertDocument(paper.toDb())
    except Exception as e:
        print(e)
        return False
    else:
        return True
        
def main(dbHost, dbName, margotPath, workingDir):
    t1 = time.time()
    modules = [ArxivPaperDownloader, BioMedArxivPaperDownloader, ResearchSquarePaperDownloader]
    db = MongoDbInstance(host = dbHost, dbName = dbName)
    mg = MargotClient(margotPath= margotPath, workingDir=workingDir)
    papers = []
    nPapers = len(papers)
    for module in modules:
        time.sleep(1)
        papers += module.getPapers()
        print("Collected {} papers from: {}".format(len(papers)-nPapers, (module.__name__.split("P")[0])))
        nPapers = len(papers)
    print("{} papers have been collected".format(len(papers)))
    keys = db.getPapersKey()    
    filteredPapers = [paper for paper in papers if paper.key not in keys]
    print("{} new papers collected!".format(len(filteredPapers)))
    if len(filteredPapers) == 0:
        print("No new paper to analyse")
        return
    inserted = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        res = []
        for paper in filteredPapers:
            res.append(executor.submit(paperPipeline, paper, mg, db))
    for r in concurrent.futures.as_completed(res):
        if r.result():
            inserted+=1
    """for paper in filteredPapers:
        time.sleep(1)
        res = paperPipeline(paper, mg, db)
        if res:
            inserted+=1"""
    print("Execution completed in {} minutes, {} inserted in the database.".format(int((time.time() - t1)/60), inserted))
    return
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--margot", "-m", action="store", help="Path to margot folder", required = True)
    parser.add_argument("--workingDir", "-wd", action="store", help="Path to the working directory to store files", required = True)
    parser.add_argument("--dbName", "-dn", action="store", help="Name of the db", required = True)
    parser.add_argument("--dbHost", "-dh", action="store", help="Host of the db", required = True)
    args = parser.parse_args()
    main(margotPath = args.margot, dbHost = args.dbHost, dbName = args.dbName, workingDir = args.workingDir)
    
    

    

    
