import sqlite3
import os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import ChatPromptTemplate

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

Settings.llm = Ollama(model="llama3.2:1b", request_timeout=120.0)

docs = SimpleDirectoryReader("data").load_data()

index = VectorStoreIndex.from_documents(docs)

chat_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a highly intelligent assistant trained to understand complex data. "
        "Your goal is to provide clear and concise answers based on the given context."
    ),
    (
        "user",
        """Context:
{context_str}

Instruction:
Answer the following query based on the context provided.

Query:
{query_str}"""
    )
])

query_engine = index.as_query_engine(text_qa_template=chat_prompt_template)

response = query_engine.query("How many departments are there currently in RVCE")

print(response)
