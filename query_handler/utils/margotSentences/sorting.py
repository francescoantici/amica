from models.QueryResult import QueryResult

class SortingFunctions:

    @staticmethod
    def sortByAverageEvidenceScore(papers):
        def sortingCriteria(elem):
            l = [sentence.evidenceScore for sentence in elem.margotSentences]
            return sum(l) / len(l)
        results = [QueryResult(paper = paper, score = sortingCriteria(paper)) for paper in papers]
        #papers.sort(key = sortingCriteria, reverse=True)
        results.sort(key = results.score, reverse= True)
        return results
    
    @classmethod
    def sortByCorrespondance(cls, papers, query):
        #CREATE VOCABULARY AND UPDATE IT, EMBEDD EVERY DOCUMENT AND STORE IT, COMPUTE THE COSINE SIMILARITY BETWEEN THE QUERY AND THE ABSTRACT
        def sortingCriteria(paper, query):
            corr = cls._correspondanceScoreCalculator(paper.margotSentences, query.keywords)
            margot = cls._margotMaxScoreCalculator(paper.margotSentences)
            return {"overall":corr*margot, "margot":margot, "correspondance":corr}
        results = [QueryResult(paper = paper, scores = sortingCriteria(paper, query)) for paper in papers]
        results.sort(key = lambda result: result.score, reverse=True)
        return [result for result in results if result.score > 0]
    
    @staticmethod
    def _margotMaxScoreCalculator(margotSentences):
        l = [max(sentence.evidenceScore, sentence.claimScore) for sentence in margotSentences]
        return sum(l) / len(l)
    
    @staticmethod
    def _correspondanceScoreCalculator(margotSentences, keywords):
        c = [sum([1 if k in sentence.text else 0 for k in keywords])/len(keywords) for sentence in margotSentences]
        return sum(c)/len(margotSentences)
        
        
    
    