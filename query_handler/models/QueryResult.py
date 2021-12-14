class QueryResult:
    
    def __init__(self, paper, scores, contains = None, missing = None):
        self.paper = paper
        self.score = scores["overall"]
        self.margotScore = scores["margot"]
        self.correspondanceScore = scores["correspondance"]
        self.contains = contains
        self.missing = missing
        