import os
import re
import subprocess
import xml.dom.minidom as dom
from subprocess import Popen
import concurrent.futures
import pandas as pd
from nltk import sent_tokenize
from services.textExtractor.grobidClient.grobidClient import GrobidClient
import time 
import requests

class TextPdfExtractor:
    
        
    @classmethod
    def _parse_introduction(cls, doc, authors_info):
        heads = doc.getElementsByTagName("head")
        head_elements = None
        warnings = 0
        figure_regex = re.compile("Figure [0-9]+:")
        table_regex = re.compile("Table [0-9]+:")

        for h in heads:
            try:
                head_text = h.childNodes[0].wholeText.strip().lower()
            except IndexError:
                continue
            head_attribute = h.getAttribute("n")
            break_after_first = False

            if head_attribute is None:
                print(
                    "[Introduction] Could not retrieve section enumeration. Focusing on first block only...Is this correct?")
                warnings += 1
                break_after_first = True

            if 'introduction' in head_text or (head_attribute is not None and head_attribute.strip().startswith("1")):
                if head_elements is None:
                    head_elements = [h]
                    if break_after_first:
                        break
                else:
                    head_elements.append(h)

        if head_elements is None:
            # Try looking for divs
            divs = doc.getElementsByTagName('div')
            for div in divs:
                if div.getAttribute('type') != 'references':
                    head_elements = [div]
                    break

            if head_elements is None:
                print("[Introduction] Could not retrieve introduction! Returning...")
                return None

        print("[Introduction] Found {} sections".format(len(head_elements)))

        text = ""

        for h_index, h in enumerate(head_elements):
            parent = h.parentNode

            # skip Introduction title
            start_index = 0 if h_index > 1 else 1
            to_explore = parent.childNodes[start_index:]

            while len(to_explore):

                child = to_explore.pop(0)

                # simple way to check Text element
                if hasattr(child, 'wholeText'):
                    child_text = child.wholeText.strip()
                    if child_text:
                        text += ' ' + child_text

                    # Check author name in text
                    if any([author_name in child_text for author_name in authors_info]):
                        print("[Introduction] Found potential header text -> ", child_text)
                        warnings += 1

                    # Check figure in text
                    found_figures = figure_regex.findall(child_text)
                    if found_figures:
                        print("[Introduction] Found some figures -> ", found_figures)
                        warnings += 1

                    # Check table in text
                    found_tables = table_regex.findall(child_text)
                    if found_tables:
                        print("[Introduction] Found some tables -> ", found_tables)
                        warnings += 1

                else:
                    if child.tagName != 'head':
                        to_explore = child.childNodes + to_explore

                    if child.tagName == 'p' and text:
                        text += "[SEP]"

            if h_index < len(head_elements) - 1:
                text += "[SEP]"

        if text.lower().startswith('introduction'):
            text = text[len('introduction'):]

        if warnings > 0:
            print("[Introduction] Total warnings -> ", warnings)

        return text

    @classmethod
    def _parse_conclusions(cls, doc, authors_info):
        heads = doc.getElementsByTagName("head")
        head_elements = None
        warnings = 0
        figure_regex = re.compile("Figure [0-9]+:")
        table_regex = re.compile("Table [0-9]+:")

        saved_head_attribute = None
        for h in heads:
            try:
                head_text = h.childNodes[0].wholeText.strip().lower()
            except IndexError:
                continue
            head_attribute = h.getAttribute("n")
            break_after_first = False

            if head_attribute is None:
                print(
                    "[Conclusions] Could not retrieve section enumeration. Focusing on first block only...Is this correct?")
                warnings += 1
                break_after_first = True

            if 'conclusions' in head_text.lower() or 'conclusion' in head_text.lower() or 'discussion' in head_text.lower() \
                    or head_attribute.split('.')[0] == saved_head_attribute:
                if head_elements is None:
                    head_elements = [h]
                    saved_head_attribute = h.getAttribute('n') if len(h.getAttribute('n').strip()) else saved_head_attribute
                    if break_after_first:
                        break
                else:
                    head_elements.append(h)

        if head_elements is None:
            print("[Conclusions] Could not retrieve conclusions! Returning...")
            return None

        print("[Conclusions] Found {} sections".format(len(head_elements)))

        text = ""

        for h_index, h in enumerate(head_elements):
            parent = h.parentNode

            # skip Introduction title
            start_index = 0 if h_index > 1 else 1
            to_explore = parent.childNodes[start_index:]

            while len(to_explore):

                child = to_explore.pop(0)

                # simple way to check Text element
                if hasattr(child, 'wholeText'):
                    child_text = child.wholeText.strip()
                    if child_text:
                        text += ' ' + child_text

                    # Check author name in text
                    if any([author_name in child_text for author_name in authors_info]):
                        print("[Introduction] Found potential header text -> ", child_text)
                        warnings += 1

                    # Check figure in text
                    found_figures = figure_regex.findall(child_text)
                    if found_figures:
                        print("[Introduction] Found some figures -> ", found_figures)
                        warnings += 1

                    # Check table in text
                    found_tables = table_regex.findall(child_text)
                    if found_tables:
                        print("[Introduction] Found some tables -> ", found_tables)
                        warnings += 1

                else:
                    if child.tagName != 'head':
                        to_explore = child.childNodes + to_explore

                    if child.tagName == 'p' and text:
                        text += "[SEP]"

            if h_index < len(head_elements) - 1:
                text += "[SEP]"

        if text.lower().startswith('conclusions'):
            text = text[len('conclusions'):]

        if warnings > 0:
            print("[Conclusions] Total warnings -> ", warnings)

        return text

    @classmethod
    def _parse_abstract(cls, doc, authors_info):
        parent = doc.getElementsByTagName("abstract")[0]

        # skip Introduction title
        to_explore = parent.childNodes
        text = ""
        warnings = 0

        while len(to_explore):

            child = to_explore.pop(0)

            # simple way to check Text element
            if hasattr(child, 'wholeText'):
                child_text = child.wholeText.strip()
                if child_text:

                    # Check author name in text
                    if any([author_name in child_text for author_name in authors_info]):
                        print("[Abstract] Found potential header text -> ", child_text)
                        warnings += 1

                        # Simple removal
                        cleaned_text = []
                        in_header = False
                        for item in sent_tokenize(child_text):
                            if all([author_name not in item for author_name in authors_info]) and not in_header:
                                cleaned_text.append(item)
                            else:
                                in_header = True
                        child_text = ' '.join(cleaned_text).strip()
                        print("[Abstract] Cleaned text -> ", child_text)

                    text += child_text
            else:
                if child.tagName != 'head':
                    to_explore = child.childNodes + to_explore

        # Some cleaning
        if text.lower().startswith('abstract'):
            text = text[len('abstract'):]
        if text.startswith('-'):
            text = text[1:]

        if warnings > 0:
            print("[Abstract] Total warnings -> ", warnings)

        return text

    @classmethod
    def _parse_authors(cls, doc):
        authors_block = doc.getElementsByTagName("fileDesc")[0]
        authors = authors_block.getElementsByTagName("author")
        authors_info = []

        for auth_section in authors:
            for child in auth_section.childNodes:
                if hasattr(child, 'tagName') and child.tagName == 'persName':
                    author_name = ""
                    for forename_block in child.childNodes:
                        try:
                            author_name += forename_block.childNodes[0].wholeText + " "
                        except IndexError as e:
                            continue
                    authors_info.append(author_name.strip())

        return authors_info

    @classmethod
    def _correct_breaks(cls, text):
        splits = text.split(os.linesep)
        splits = map(lambda item: item.strip().replace(os.linesep, '').replace('[SEP]', '{0}{0}'.format(os.linesep)),
                    splits)
        splits = filter(lambda item: len(item) > 0, splits)
        splits = list(splits)

        return ' '.join(splits)

    @classmethod
    def _expand_with_separators(cls, text, sentence_threshold=4):
        expanded_text = ""
        splits = sent_tokenize(text)

        start_idx = 0
        end_idx = sentence_threshold

        while start_idx < len(splits):
            chunk = splits[start_idx:end_idx]
            if chunk:
                expanded_text += ' '.join(chunk) + os.linesep + os.linesep

            start_idx = end_idx
            end_idx += sentence_threshold

        expanded_text = expanded_text.strip()

        return expanded_text

    @classmethod
    def parse_xml(cls, xml):
        """with open(filename) as xml:
            doc = dom.parse(xml)"""
        doc = dom.parseString(xml)
        doc = doc.childNodes[0]

        title = doc.getElementsByTagName("title")[0].childNodes[0].nodeValue
        authors_info = cls._parse_authors(doc)
        try:
            abstract = cls._parse_abstract(doc, authors_info)
        except IndexError as e:
            print("Grobid parsing encountered an error! Abstract could not be retrieved")
            raise e

        try:
            introduction = cls._parse_introduction(doc, authors_info)
        except IndexError as e:
            print("Grobid parsing encountered an error! Introduction could not be retrieved")
            raise e

        try:
            conclusions = cls._parse_conclusions(doc, authors_info)
        except IndexError as e:
            print("Grobid parsing encountered an error! Conclusions could not be retrieved")
            raise e

        title = cls._correct_breaks(title)
        if abstract is not None:
            abstract = cls._correct_breaks(abstract)
            abstract = cls._expand_with_separators(abstract)

        if introduction is not None:
            introduction = cls._correct_breaks(introduction)
            introduction = cls._expand_with_separators(introduction)

        if conclusions is not None:
            conclusions = cls._correct_breaks(conclusions)
            conclusions = cls._expand_with_separators(conclusions)

        if (abstract is not None and 'email' in abstract) or (introduction is not None and 'email' in introduction):
            print("Found Email section in abstract or in introduction. Please check the parsed paper.")

        return title, abstract, introduction, conclusions

    @classmethod
    def extractBatch(cls, fileNames, bufferedPdfs): 
        client = GrobidClient()
        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
            results = []
            for i in range(len(bufferedPdfs)):
                time.sleep(1)
                r = executor.submit(
                    client.process_pdf,
                    "processFulltextDocument",
                    fileNames[i],
                    bufferedPdfs[i],
                    generateIDs=False,
                    consolidate_header=True,
                    consolidate_citations=False,
                    include_raw_citations=False,
                    include_raw_affiliations=False,
                    tei_coordinates=False,
                    segment_sentences=False 
                    
                )
                results.append(r)
        xmlList = []
        for r in concurrent.futures.as_completed(results):
            input_file, status, text = r.result()

            if text is None:
                continue
            else:
                xmlList.append(text)
        errors = 0
        texts = {}
        for i in range(len(xmlList)):
            try:
                title, abstract, introduction, conclusions = cls.parse_xml(xmlList[i])
                if abstract is None:
                    abstract = ""
                    errors += 1

                if introduction is None:
                    introduction = ""
                    errors += 1

                if conclusions is None:
                    conclusions = ""
                    errors += 1
            except Exception as e:
                print(e)
                continue                
            texts[fileNames[i]] = title+"\n"+abstract+"\n"+introduction+"\n"+conclusions
        print("Total errors: ", errors)
        return texts 
    
    
    @classmethod
    def extractFile(cls, fileName, data):
        client = GrobidClient()        
        _, _, xml = client.process_pdf(
                "processFulltextDocument", fileName, data, generateIDs=False,
                    consolidate_header=True,
                    consolidate_citations=False,
                    include_raw_citations=False,
                    include_raw_affiliations=False,
                    tei_coordinates=False,
                    segment_sentences=False
            )
        
        if xml is None:
            return None
        errors = 0
        try:
            title, abstract, introduction, conclusions = cls.parse_xml(xml)
            if abstract is None:
                abstract = ""
                errors += 1

            if introduction is None:
                introduction = ""
                errors += 1

            if conclusions is None:
                conclusions = ""
                errors += 1
        except Exception as e:
            print(e)
            return 
        else:    
            print("*" * 50)
            print("Total errors: ", errors)           
            return title+"\n"+abstract+"\n"+introduction+"\n"+conclusions
         
        
        

            

        

        
                

                

                

                

        
