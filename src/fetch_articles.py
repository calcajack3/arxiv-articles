import urllib.request
from xml.etree import cElementTree as ET
from typing import List, Tuple

# Function to fetch XML data from a URL


def fetch_xml_data(url: str) -> str:
    data = urllib.request.urlopen(url)
    xml_data = data.read().decode('utf-8')
    return xml_data

# Function to extract titles and summaries from XML data


Article = Tuple[str, str, str]


def extract_titles_and_summaries(xml_data: str) -> List[Article]:
    root = ET.fromstring(xml_data)

    # Initialize an empty list to store the tuples of title, summary, and link
    title_summary_pairs: List[Article] = []

    # Iterate over each entry in the XML data
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        # Extract the title and summary text from each entry
        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text or ""
        summary = entry.find(
            './/{http://www.w3.org/2005/Atom}summary').text or ""
        summary = summary.replace('\n', ' ')
        link = entry.find(
            './/{http://www.w3.org/2005/Atom}link').attrib['href']

        # Append the tuple (title, summary, link) to the list
        title_summary_pairs.append((title, summary, link))

    return title_summary_pairs

# Function to get papers from a URL


def get_papers(url: str) -> List[Tuple[str, str, str]]:
    xml_data = fetch_xml_data(url)
    titles_summaries = extract_titles_and_summaries(xml_data)
    return titles_summaries
