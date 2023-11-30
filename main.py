from src.fetch_articles import fetch_xml_data, extract_titles_and_summaries
from src.embed import VectorDB

results: int = 10
url: str = f'http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results={results}'


def main():
    xml_data = fetch_xml_data(url)
    articles = extract_titles_and_summaries(xml_data)
    db = VectorDB()
    db.embed_articles(articles)
    # stored_articles = db.get_all_articles()
    # print(stored_articles)
    results = db.get_articles_from_query('llm large language models ai prompting', 1)
    print(results[0])
    


if __name__ == '__main__':
    main()
