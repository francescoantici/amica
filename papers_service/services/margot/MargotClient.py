from subprocess import Popen
from models.MargotSentence import MargotSentence
import os
import json

class MargotClient:
    
    def __init__(self, margotPath, outPath = "results_margot", workingDir = None):
        self.margotPath = margotPath
        if not(workingDir):
            self.globalWorkingDir = os.path.join(self.margotPath, outPath)
        else:
            self.globalWorkingDir = workingDir
        if not(os.path.isdir(self.globalWorkingDir)):
            os.mkdir(self.globalWorkingDir)
        if not(os.path.isdir(self.globalWorkingDir+"/output")):
            os.mkdir(self.globalWorkingDir+"/output")
        if not(os.path.isdir(self.globalWorkingDir+"/input")):
            os.mkdir(self.globalWorkingDir+"/input")
        if not(os.path.isdir(self.globalWorkingDir+"/output/html")):
            os.mkdir(self.globalWorkingDir+"/output/html")
        if not(os.path.isdir(self.globalWorkingDir+"/output/xml")):
            os.mkdir(self.globalWorkingDir+"/output/xml")
        if not(os.path.isdir(self.globalWorkingDir+"/output/txt")):
            os.mkdir(self.globalWorkingDir+"/output/txt")
        if not(os.path.isdir(self.globalWorkingDir+"/output/json")):
            os.mkdir(self.globalWorkingDir+"/output/json")
        
    def annotate(self, text, fileName):
        tmpFile = os.path.join(self.globalWorkingDir, ".txt")
        with open(tmpFile, "w") as f:
            f.write(text)
        
        print("Analysing {} with margot...".format(fileName))
        p1 = Popen("cat {}/resources/web/header.html > {}/output/html/{}.html".format(os.getcwd(), self.globalWorkingDir, fileName))
        p1.wait()
        process = Popen('bash ./run_margot.sh {} {} >> {}/output/html/{}.html'.format(tmpFile, self.globalWorkingDir, self.globalWorkingDir, fileName),
                        shell=True, cwd=self.margotPath)
        process.wait()
        p2 = Popen("echo '</body></html>' >> {}/output/html/{}.html".format(self.globalWorkingDir, fileName))
        p2.wait()
        print("{} processed sucessfully with margot.".format(fileName))
        os.rename(os.path.join(self.globalWorkingDir,"input/input.txt"), os.path.join(self.globalWorkingDir,"input/{}.txt".format(fileName)))
        os.rename(os.path.join(self.globalWorkingDir,"output/json/OUTPUT.json"), os.path.join(self.globalWorkingDir,"output/json/{}.json".format(fileName)))
        os.rename(os.path.join(self.globalWorkingDir,"output/xml/OUTPUT.xml"), os.path.join(self.globalWorkingDir,"output/xml/{}.xml".format(fileName)))
        os.rename(os.path.join(self.globalWorkingDir,"output/txt/OUTPUT.txt"), os.path.join(self.globalWorkingDir,"output/txt/{}.txt".format(fileName)))
        with open(os.path.join(os.path.join(self.globalWorkingDir, "output/json"), "{}.json".format(fileName))) as f:
            doc = json.loads(f.read())
        os.remove(tmpFile)        
        return [MargotSentence.fromJson(entry) for entry in doc['document']]

            
        
    
        