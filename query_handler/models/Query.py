import string

class Query:
    
    def __init__(self, query):
        self.keywords = [word.strip() for word in query.split(" ") if word not in string.punctuation]