import urllib.request
from xml.etree import cElementTree as ET


def fetch_xml_data(url):
    data = urllib.request.urlopen(url)
    xml_data = data.read().decode('utf-8')
    return xml_data


def extract_titles(xml_data):
    root = ET.fromstring(xml_data)
    titles = [title.text for title in root.findall(
        './/{http://www.w3.org/2005/Atom}title')][1:]
    return titles


def get_papers(url):
    xml_data = fetch_xml_data(url)
    titles = extract_titles(xml_data)
    return titles
