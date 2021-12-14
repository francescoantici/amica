from models.Paper import Paper

class ArxivPaper(Paper):
    
    source = "arxiv"
    
    @staticmethod
    def fromXml(entry, namespaces):
        fetchInEntry = lambda field: entry.find("feed:{}".format(field), namespaces).text
        authors = [author.find('feed:name', namespaces).text for author in entry.findall('feed:author', namespaces)]
        pdfLink = None
        for link in entry.findall('feed:link', namespaces):
            if link.attrib.get("title") == "pdf":
                pdfLink = link.attrib.get("href") + ".pdf"
        return ArxivPaper(title = fetchInEntry("title"), authors = authors, published = fetchInEntry("published"),
                          link = fetchInEntry("id"), pdf = pdfLink, summary = fetchInEntry("summary"))
        