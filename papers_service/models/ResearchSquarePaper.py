from models.Paper import Paper

class ResearchSquarePaper(Paper):
    
    source = "researchsquare"
    
    def _generateKey(self):
        return self.source + "_" + self.link.split("/")[-2]
    
    @staticmethod
    def fromJson(json):
        published = (json['posted_at'].split(" ")[0]).split("-")
        published.reverse()
        link = "https://www.researchsquare.com/article/{}/v{}".format(json['article_identity'], json['doi_version'])
        return ResearchSquarePaper(title = json['title'], authors = [author.strip() for author in json['authors'].split(',')], published = "/".join(published),
                                   link = link, pdf = link+".pdf")