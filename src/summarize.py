from src.fetch_articles import Article
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class Summarizer():
    """
    A class to summarize articles
    """

    def __init__(self):
        self.chat_model = ChatOpenAI()
        self.prompt_template = ChatPromptTemplate.from_template(
            """make an understandable explanatory structured summary in 3 main points of the following abstract, **focus ONLY on: What is achieved?, How it is done?, and Why it is important?**, this should be for an article for a tech newsletter, NEVER put a heading at top, ONLY the CONTENT explanation. output MUST be in structured HTML format, make a list and bolded some keywords: 
            {abstract}""")
        self.chain = self.prompt_template | self.chat_model

    def summarize_article(self, article: Article) -> Article:
        """
        Summarize an article
        :param article: An article to summarize
        :return: The article with the summary added
        """
        summary = self.chain.invoke({'abstract': article.abstract})
        article.set_summary(summary.content)
        return article

    def summarize_articles(self, articles: list[Article]) -> list[Article]:
        """
        Summarize a list of articles
        :param articles: A list of articles to summarize
        :return: A list of summaries of the articles
        """
        articles_with_summary: list[Article] = []
        
        for article in articles:
            articles_with_summary.append(self.summarize_article(article))
        
        return articles_with_summary