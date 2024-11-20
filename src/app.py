import os
import streamlit as st
from indexing import indexer, build_and_save_index
import json

# Load professor profiles from JSON file
with open("data/profile.json") as f:
    profiles = json.load(f)

def get_professor_profile(query):
    query = query.lower()
    for professor in profiles["professors"]:
        full_name = professor["name"].lower()
        designations = ["dr.", "prof.", "mr.", "mrs.", "ms."]
        actual_name = full_name
        for designation in designations:
            actual_name = actual_name.replace(designation, "").strip()
        if actual_name in query:
            return professor
    return None

def render_html_template(template_path, context):
    with open(template_path, "r") as file:
        template = file.read()
    for key, value in context.items():
        template = template.replace(f"{{{{ {key} }}}}", value)
    return template

# Sidebar information
with st.sidebar:
    st.title("RV-ASSIST")
    st.subheader("Aayaan Hasnain 1RV21AI001")
    st.subheader("Akshay Alva 1RV21AI007")  

# Title and introductory text
st.title("💬 RV-Assist")
st.caption("🚀 LLM used for demo: Llama 3.2:1b")

# Initialize session states
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
    with open("templates/map.html", "r") as f:
        map_html = f.read()
    st.components.v1.html(map_html, width=1000, height=600)

# Prompt input
if prompt := st.chat_input("Ask me anything!"):
    professor_profile = get_professor_profile(prompt)
    if professor_profile:
        with st.chat_message("user"):
            st.markdown(prompt)  # Display the user's input
            st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            context = {
                "name": professor_profile["name"],
                "image_url": professor_profile["image_url"],
                "department": professor_profile["department"],
                "designation": professor_profile["designation"],
                "research_interests": professor_profile["research_interests"],
                "link": professor_profile["link"],
            }
            profile_html = render_html_template("templates/professor_profile.html", context)
            st.components.v1.html(profile_html, height=800)
            st.session_state.messages.append({"role": "assistant", "content": "Professor profile displayed."})

        # Exit early to prevent forwarding to LLM
        exit()

    # If no professor is found, proceed with LLM query
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
