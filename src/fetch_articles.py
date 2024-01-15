import urllib.request
from xml.etree import cElementTree as ET

# Define the Article class
class Article:
    def __init__(self, title: str, abstract: str, link: str):
        self.title = title
        self.abstract = abstract
        self.link = link
        self.id = link.split('/')[-1]
        self.summary = ""
    
    @classmethod
    def from_document(cls, document):
        """
        Alternative constructor to create an Article object from a document.

        :param document: A document object.
        :return: An instance of Article.
        """
        try:
            title = document.metadata['title']
            abstract = document.page_content
            link = document.metadata['link']
        except AttributeError:
            try:
                title = document['metadatas'][0]['title']
                abstract = document['documents'][0]
                link = document['metadatas'][0]['link']
            except:
                return None
        return cls(title, abstract, link)
    
    def set_summary(self, summary: str):
        """
        Sets the summary of the article.

        :param summary: A summary of the article.
        """
        self.summary = summary

# Function to fetch XML data from a URL
def fetch_xml_data(url: str) -> str:
    """
    Fetches XML data from a URL and returns it as a string.
    :param url: URL to fetch XML data from.
    :return: XML data as a string.
    """
    data = urllib.request.urlopen(url)
    xml_data = data.read().decode('utf-8')
    return xml_data

# Function to extract titles, abstracts, and links from XML data
def extract_titles_and_summaries(xml_data: str) -> list[Article]:
    """
    Extracts titles, abstracts, and links from XML data and returns them as a list of Article objects.
    :param xml_data: XML data as a string.
    :return: List of Article objects.
    """
    root = ET.fromstring(xml_data)

    articles = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text or ""
        abstract = entry.find('.//{http://www.w3.org/2005/Atom}summary').text or ""
        abstract = abstract.replace('\n', ' ').strip()
        link = entry.find('.//{http://www.w3.org/2005/Atom}link').attrib['href']

        articles.append(Article(title, abstract, link))

    return articles

# Function to get papers from a URL
def get_papers(url: str) -> list[Article]:
    """
    Fetches XML data from a URL and returns a list of Article objects.
    :param url: URL to fetch XML data from.
    :return: List of Article objects.
    """
    xml_data = fetch_xml_data(url)
    articles = extract_titles_and_summaries(xml_data)
    return articles
