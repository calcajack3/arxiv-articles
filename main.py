from fetch_articles import fetch_xml_data, extract_titles

url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=10'


def main():
    xml_data = fetch_xml_data(url)
    titles = extract_titles(xml_data)
    print(titles)


if __name__ == '__main__':
    main()
