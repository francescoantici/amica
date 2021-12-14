from models.Paper import Paper

class BioMedArxivPaper(Paper):
    
    source = "biomedarxiv"
    
    @staticmethod
    def fromXml(item, namespaces):
        authors = [author.text for author in item.findall("dc:creator", namespaces)]
        date = item.find("dc:date", namespaces).text.split("-")
        date.reverse()
        published = "/".join(date)
        link = item.attrib.get("{"+namespaces['rdf']+"}about")
        return BioMedArxivPaper(title = item.find("xmlns:title", namespaces).text, authors = authors, published = published,
                                link = link, pdf = link+".full.pdf", summary = item.find("xmlns:description", namespaces).text)
        
    @staticmethod
    def fromJson(json):
        date = json["rel_date"].split("-")
        date.reverse()
        published = "/".join(date)
        link = json["rel_link"].replace("\/", "/")
        try:
            authors = [author["author_name"] for author in json["rel_authors"]]
        except:
            authors = []
        return BioMedArxivPaper(title = json["rel_title"], authors=authors, 
                                published=published, link = link, pdf = link+".full.pdf",
                                summary = json["rel_abs"])