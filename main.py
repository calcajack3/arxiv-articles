from src.fetch_articles import fetch_xml_data, extract_titles_and_summaries

results: int = 2
url: str = f'http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results={results}'


def main():
    xml_data = fetch_xml_data(url)
    articles = extract_titles_and_summaries(xml_data)
    print(articles[0])


if __name__ == '__main__':
    main()
