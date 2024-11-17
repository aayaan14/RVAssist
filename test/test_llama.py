import sqlite3
import os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

Settings.llm = Ollama(model="llama3.2:1b", request_timeout=360.0)

docs = SimpleDirectoryReader("data").load_data()

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()

response = query_engine.query("What is RVCE")

print(response)
