from src.fetch_articles import Article
from src.fetch_articles import fetch_xml_data, extract_titles_and_summaries
from src.embed import VectorDB
from src.summarize import Summarizer
from src.email import Email
from markdown2 import markdown

results: int = 50
url: str = f'http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results={results}'

n_selected_articles: int = 3

def main():
    xml_data = fetch_xml_data(url)
    articles = extract_titles_and_summaries(xml_data)
    db = VectorDB()
    db.embed_articles(articles)
    # stored_articles = db.get_all_articles()
    # print(stored_articles)
    
    results = db.get_articles_from_query('llm large language models generative ai prompt prompting', n_selected_articles)

    summarizer = Summarizer()
    articles_with_summary: list[Article] = summarizer.summarize_articles(results)
    print(articles_with_summary[0].summary)
    email = Email()
    email.prepare_email(articles_with_summary, n_selected_articles)
    email.send_email("calcajack@gmail.com")


if __name__ == '__main__':
    main()
