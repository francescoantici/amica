from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import os

class Body:
    
    @staticmethod
    def createHTML(resultList, htmlPath, query, htmlTemplate = "body.html"):
        env = Environment(loader=PackageLoader("web"), autoescape=select_autoescape())
        def datetime_format(result):
            if result.source == "arxiv":
                return datetime.strptime(result.published, "%Y-%m-%dT%H:%M:%SZ").strftime("%m/%Y")
            return result.published
        env.filters["datetime_format"] = (lambda result: datetime_format(result))
        env.filters["margot_html_format"] = (lambda key: os.path.join(htmlPath, key+".html"))
        env.filters["format_score_function"] =  (lambda result: "{:.4f}".format(result))   
        template = env.get_template(htmlTemplate)
        return template.render(results = resultList, query = query)