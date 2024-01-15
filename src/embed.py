import os
from dotenv import load_dotenv
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .fetch_articles import Article  # Ensure this import is correct

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VectorDB:
    
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.db = Chroma(embedding_function=self.embeddings_model, persist_directory=f'db')

    def embed_article(self, article: Article):
        """
        Embeds an article and stores it in the DB
        :param article: An article to embed
        :return: The embedded article
        """
        print('Checking if article already in DB')
        if self.get_article_by_id(article.id):
            print('Article already in DB')
            return
        
        print('Embedding Article...')
        title_vector, abstract_vector = self.embeddings_model.embed_documents([article.title, article.abstract])
        
        title_vector_np = np.array(title_vector)
        abstract_vector_np = np.array(abstract_vector)
        
        article_vector = (2 * title_vector_np + abstract_vector_np) / 3
        article_vector = article_vector.tolist()

        self.store_article(article, article_vector)

    def store_article(self, article: Article, article_vector):
        """
        Stores an article in the DB
        :param article: An article to store
        """
        self.db._collection.add(ids=[article.id], embeddings=[article_vector], documents=[article.abstract], metadatas=[{'title': article.title, 'link': article.link}])
        self.db.persist()

    def embed_articles(self, articles: list[Article]):
        """
        Embeds a list of articles and stores them in the DB
        :param articles: A list of articles to embed
        :return: The embedded articles
        """
        for article in articles:
            self.embed_article(article)

    def embed_sentence(self, sentence: str):
        """
        Embeds a sentence and stores it in the DB
        :param sentence: A sentence to embed
        """
        self.db.add_texts(texts=[sentence])
    
    def get_all_articles(self):
        """
        Returns all articles in the DB
        :return: All articles in the DB
        """
        documents = self.db._collection.get()

        articles: list[Article] = []

        for document in documents:
            articles.append(Article.from_document(document))

        return articles

    def get_article_by_id(self, id: str):
        """
        Returns an article by its ID
        :param id: ID of the article to return
        :return: The article with the given ID
        """

        document = self.db._collection.get(ids=id)
        return Article.from_document(document)

    def get_articles_from_query(self, query: str, k: int = 10):
        """
        Returns the k most similar articles to a query
        :param query: Query to search for
        :param k: Number of articles to return
        :return: The k most similar articles to the query
        """
        documents = self.db.similarity_search(query, k)

        articles: list[Article] = []

        for document in documents:
            articles.append(Article.from_document(document))

        return articles