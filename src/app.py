import os
import streamlit as st
from indexing import indexer, build_and_save_index

# Sidebar information
with st.sidebar:
    st.title("EL-DEMO")
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
            Currently, my knowledge base is built from structured data like PDFs and SQLite databases.
            """,
        }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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

# Button to rebuild the index
if st.button("Rebuild Index"):
    try:
        build_and_save_index()
        st.success("Index rebuilt successfully!")
    except Exception as e:
        st.error(f"Failed to rebuild index: {e}")

# Button to show the college map
map_url = "http://127.0.0.1:5500/map.html"
if st.button("Show College Map"):
    st.components.v1.iframe(map_url, width=900, height=700)
