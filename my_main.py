import streamlit as st
import os
from dotenv import load_dotenv
from backend.my_core import run_llm
from typing import Set
from streamlit_chat import message
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Documentation",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match LangChain documentation style
st.markdown("""
    <style>
    /* Main page styles */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Header styles */
    .stMarkdown h1 {
        font-size: 2.5rem;
        font-weight: 600;
        color: #111827;
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background-color: #F3F4F6;
    }
    
    /* Input field styles */
    .stTextInput > div > div > input {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 0.375rem;
        color: #111827;
    }
    
    /* Button styles */
    .stButton > button {
        background-color: #7C3AED;
        color: white;
        border: none;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
    }
    
    /* Chat message styles */
    .stTextArea > div > div > textarea {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 0.375rem;
        color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

load_dotenv()

# Initialize session state for user profile
if 'user_name' not in st.session_state:
    st.session_state.user_name = 'John Doe'
if 'user_email' not in st.session_state:
    st.session_state.user_email = 'john.doe@example.com'
if 'profile_picture' not in st.session_state:
    st.session_state.profile_picture = "https://www.w3schools.com/howto/img_avatar.png"

# Sidebar with LangChain style
with st.sidebar:
    st.title("Documentation")
    st.divider()
    
    # User profile section
    st.subheader("User Profile")
    st.image(st.session_state.profile_picture, width=100)
    uploaded_file = st.file_uploader("Update Profile Picture", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        st.session_state.profile_picture = uploaded_file
    
    new_name = st.text_input("Name", value=st.session_state.user_name, 
                            key="name_input",
                            help="Click to edit your name")
    new_email = st.text_input("Email", value=st.session_state.user_email,
                             key="email_input",
                             help="Click to edit your email")
    
    st.session_state.user_name = new_name
    st.session_state.user_email = new_email

# Main content area
st.title("🦜 LangChain Ask the Quran Helper")

# Initialize chat states
if 'something' not in st.session_state:
    st.session_state.something = ''
if 'prompt' not in st.session_state:
    st.session_state.prompt = ''
if "user_prompt_history" not in st.session_state:
    st.session_state.user_prompt_history = []
if "chat_answers_history" not in st.session_state:
    st.session_state.chat_answers_history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def submit():
    st.session_state.something = st.session_state.prompt
    st.session_state.prompt = ''

# Chat interface
st.markdown("### 💬 Ask a Question")
col1, col2 = st.columns([6, 1])
with col1:
    st.text_input('', key='prompt', on_change=submit, 
                 placeholder='Ask anything about God...',
                 label_visibility="collapsed")
with col2:
    st.markdown("📤")

prompt = st.session_state.something

def create_sources_string(sources: set[str]) -> str:
    if not sources:
        return "No sources"
    sources_list = list(sources)
    sources_list.sort()
    sources_string = "Sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

if prompt:
    with st.spinner(f"Searching documentation for: {prompt}"):
        response = run_llm(query=prompt, chat_history=st.session_state.chat_history)
        sources = set([doc.metadata["source"] for doc in response["source_documents"]])
        formatted_response = (
            f"{response['result']}\n\n{create_sources_string(sources)}"
        )
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(formatted_response)
        st.session_state.chat_history.append(prompt)
        st.session_state.chat_history.append(response['result'])

# Display chat history
if st.session_state.user_prompt_history:
    st.markdown("### Chat History")
    for i, (prompt, response) in enumerate(
        zip(st.session_state.user_prompt_history, st.session_state.chat_answers_history)
    ):
        # User message
        message(prompt, is_user=True, key=f"user_{i}")
        
        # Assistant message
        message(response, is_user=False, key=f"assistant_{i}")
        
        st.divider()
