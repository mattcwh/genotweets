import requests
from xml.etree import cElementTree as ElementTree
from json import dumps

# retrieve pubmed ID with designated author keywords

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)

class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

def FindPMIDWithKeyword(keyword_list, field_tag, db="pubmed", retmax=100):
    """
    takes keywords, transforms into url for a request from API
    returns a list of PMID with those author keywords
    **not MeSH
    """
    #generate query string from keywords list
    query_items = []

    for i in keyword_list:
        if i != keyword_list[-1]:
            i = i + "[" + field_tag + "]"
            single_word = i.split()
            query_items.extend(single_word)
            query_items.append("OR")
        else:
            i = i + "[" + field_tag + "]"
            single_word = i.split()
            query_items.extend(single_word)

    query_string = "+".join(query_items)

    #generate url to access esearch API
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + "db=" + db + "&retmode=json" + "&retmax=" + str(retmax) + "&term=" + query_string

    #request and morph into a list of strings of PMID
    r = requests.get(url)
    r_to_dict = r.json()
    PMID_list_unicode = r_to_dict['esearchresult']['idlist']
    PMID_list = map(lambda x: x.encode('ascii', 'ignore'), PMID_list_unicode)

    return PMID_list

def FindAllKeywordsFromPMID(PMID_list, db="pubmed"):
    """
    takes PMID list, iterates throughout and select all author keywords
    returns list of lists of OT (Other Terms, author defined keywords)
    """

    #URL length exceeds capacity limit, fetch OT__ with PMID_list individually
    returned_OT = []

    for PMID in PMID_list:
        url2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + "db=" + db + "&retmode=xml" + "&id=" + PMID
        r2 = requests.get(url2)
        r2_root = ElementTree.XML(r2.text.encode("utf-8"))
        r2_to_dict = XmlDictConfig(r2_root)
        returned_OT.append(r2_to_dict["PubmedArticle"]["MedlineCitation"]["KeywordList"]["Keyword"])

    return returned_OT

if __name__ == "__main__":

    keywords = ["genetic test", "genetic testing", "genomic test", "genomic testing",
                "DNA test", "DNA testing", "genetic screening", "personal genomics"]

    PMID_list = FindPMIDWithKeyword(keywords, "ot", retmax=5000)
    print(len(PMID_list))

    AssociatedOT = FindAllKeywordsFromPMID(PMID_list[:10])
    print(AssociatedOT[:10])
