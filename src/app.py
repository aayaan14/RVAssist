import os
from dotenv import load_dotenv
from embedchain import App
import streamlit as st

load_dotenv()

HUGGINGFACE_ACCESS_TOKEN = os.getenv("HUGGINGFACE_ACCESS_TOKEN")

app = App()
