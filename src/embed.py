import os
from dotenv import load_dotenv
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .fetch_articles import Article

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VectorDB:
    
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.db = Chroma(embedding_function=self.embeddings_model, persist_directory='db')

    def embed_article(self, article: Article):
        
        print('Checking if article already in DB')
        if self.get_article_by_id(article[2])['ids']:
            print('Article already in DB')
            return self.get_article_by_id(article[2])
        
        print('Embedding Article')
        title_vector, abstract_vector = self.embeddings_model.embed_documents(article[:2])
        
        title_vector_np = np.array(title_vector)
        abstract_vector_np = np.array(abstract_vector)
        
        article_vector = (2 * title_vector_np + abstract_vector_np) / 3
        article_vector = article_vector.tolist()

        self.db._collection.add(ids=[article[2]], embeddings=[article_vector], documents=[article[1]], metadatas=[{'title': article[0], 'link': article[2]}])
        self.db.persist()
        return article_vector

    def embed_articles(self, articles: list):
        for article in articles:
            self.embed_article(article)

    def embed_sentence(self, sentence: str) -> list:
        self.db.add_texts(texts=[sentence])
    
    def get_all_articles(self):
        return self.db._collection.get()

    def get_article_by_id(self, id: str):
        return self.db._collection.get(ids=id)

    def get_articles_from_query(self, query: str, k: int = 10):
        return self.db.similarity_search(query, k)
        
