import sqlite3
import os
from dotenv import load_dotenv

import torch

from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from llama_index.core import ChatPromptTemplate

load_dotenv()

HUGGINGFACE_ACCESS_TOKEN = os.getenv('HUGGINGFACE_ACCESS_TOKEN')

def load_content_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch Content
    cursor.execute("SELECT url, content FROM web_pages")
    data = cursor.fetchall()

    # Prepare for LlamaIndex
    docs = [{'url': row[0], 'content': row[1]} for row in data]

    return docs

# quantization_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     # bnb_4bit_compute_dtype=torch.float16,
#     # bnb_4bit_quant_type="nf4",
#     # bnb_4bit_use_double_quant=True,
# )

Settings.llm = HuggingFaceLLM(
    model_name='mistralai/Mistral-7B-Instruct-v0.1',
    context_window=3900,
    max_new_tokens=128,
    # model_kwargs={'quantization_config':quantization_config},
    generate_kwargs={"temperature":0.3, "top_k": 50, "top_p": 0.95},
    device_map='cuda'
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

prompt = [
    (
        "user",
        """You are a Q&A assistant. Your goal is to answer questions as
accurately as possible based on the instructions and context provided.

        Context:

        {context_str}

        Question:

        {query_str}
""",
    )
]

text_qa_template = ChatPromptTemplate.from_messages(prompt)

def create_index(data_directory: str, index_save_path: str):
    if not os.path.exists(data_directory):
        raise ValueError(f"Data directory '{data_directory}' does not exist.")
    
    # Load documents from the directory
    print("Loading documents...")
    documents = SimpleDirectoryReader(data_directory).load_data()

    # Build the index
    print("Building the index...")
    index = VectorStoreIndex.from_documents(
        documents,
        llm=Settings.llm,
        embed_model=Settings.embed_model
    )

    # Save the index
    print(f"Saving index to '{index_save_path}'...")
    index.save(index_save_path)

    print("Index created and saved successfully.")
    return index

# Function to Query the Index
def query_index(index_path: str, query: str):
    if not os.path.exists(index_path):
        raise ValueError(f"Index file '{index_path}' does not exist.")
    
    # Load the saved index
    print("Loading index...")
    index = VectorStoreIndex.load(index_path)
    
    # Create query engine
    print("Creating query engine...")
    query_engine = index.as_query_engine(text_qa_template=text_qa_template)
    
    # Query the engine
    print(f"Querying: {query}")
    response = query_engine.query(query)
    return response

if __name__ == "__main__":
    DATA_DIR = "./data"
    INDEX_PATH = "./index.json"

    # Step 1: Create Index
    create_index(DATA_DIR, INDEX_PATH)

    # Step 2: Query the Index
    question = "Why is steam a good servant, but a terrible master?"
    answer = query_index(INDEX_PATH, question)
    print(f"Answer: {answer}")