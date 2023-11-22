import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def embed_documents(documents: list[str]) -> list:
    return embeddings_model.embed_documents(documents)