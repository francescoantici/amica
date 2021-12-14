from models.Paper import Paper

class PubMedPaper(Paper):
    
    @staticmethod
    def fromXml(entry):
        fetchInEntry = lambda field: entry.find(field).text
        authors = [author.find('LastName').text + " " +  author.find('ForeName').text for author in entry.find('AuthorList').findall('Author')]
        pdfLink = None
        doiLink = None
        for link in entry.findall('ArticleId '):
            if link.attrib.get("IdType") == "doi":
                doiLink = link.text
        return PubMedPaper(title = fetchInEntry("ArticleTitle"), authors = authors, published = fetchInEntry("published"),
                          link = doiLink, summary = fetchInEntry("summary"))