import os
import streamlit as st
from indexing import indexer, build_and_save_index

# Sidebar information
with st.sidebar:
    st.title("RV-ASSIST")
    st.subheader("Aayaan Hasnain 1RV21AI001")
    st.subheader("Akshay Alva 1RV21AI007")  

# Title and introductory text
st.title("💬 RVChat")
st.caption("🚀 LLM used for demo: Llama 3.2:1b")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
            Hello professors! I'm a model chatbot. I can answer anything you want to know about RVCE.
            Currently, my knowledge base is built from structured data like HTML files, PDFs.
            """,
        }
    ]

if "show_map" not in st.session_state:
    st.session_state.show_map = False  # Initialize map visibility state

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add a button to toggle the map display
if st.button("Toggle Map"):
    st.session_state.show_map = not st.session_state.show_map  # Toggle the map state

# Display the map if the state is True
if st.session_state.show_map:
    with open("src/map.html", "r") as f:
        map_html = f.read()
    st.components.v1.html(map_html, width=1000, height=600)

# Prompt input
if prompt := st.chat_input("Ask me anything!"):
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # Placeholder for the assistant's message
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")

        # Call the indexer function from indexing.py
        try:
            response = indexer(prompt)
            msg_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"An error occurred: {e}"
            msg_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
