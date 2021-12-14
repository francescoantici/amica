class MargotSentence:
    
    def __init__(self, text, evidenceScore, claimScore, isClaim = False, isEvidence = False):
        self.text = text 
        self.evidenceScore = evidenceScore
        self.claimScore = claimScore
        self.isClaim = isClaim
        self.isEvidence = isEvidence
    
    @staticmethod
    def fromJson(entry):
        evidenceScore = float(entry['evidence_score'])
        claimScore = float(entry['claim_score'])
        return MargotSentence(text = entry['text'], evidenceScore = evidenceScore, claimScore = claimScore, 
                              isClaim = (claimScore > 0), isEvidence = (evidenceScore > 0))
        